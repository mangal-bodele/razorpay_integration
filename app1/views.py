from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import Coffee
import razorpay
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from twilio.rest import Client

# Function to generate the invoice PDF
def generate_invoice(order_id, total_amount):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Invoice #{order_id}")
    p.drawString(100, 730, f"Total: ₹{total_amount}")
    p.showPage()
    p.save()

    buffer.seek(0)

    # Save the invoice to a path in your media folder
    file_path = f"media/invoices/invoice_{order_id}.pdf"  # Update with your actual media path
    with open(file_path, "wb") as f:
        f.write(buffer.read())

    return f"https://yourdomain.com/{file_path}"  # Replace with the actual URL to the PDF

# Function to send SMS with invoice link using Twilio
def send_sms_with_invoice(phone_number, order_id, total_amount):
    invoice_url = generate_invoice(order_id, total_amount)

    # Twilio client setup
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Send SMS
    try:
        message = client.messages.create(
            body=f"Your invoice is ready! View it here: {invoice_url}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return message.sid  # Return the message SID for success tracking
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return None

# Home view to handle coffee orders
def home_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity', 1))
        drink_option = request.POST.get('drink_option')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')  # Add phone number field to the form
        
        # Define coffee prices
        drink_prices = {
            'espresso': 100,
            'latte': 150,
            'cappuccino': 120,
            'americano': 110,
            'mocha': 160
        }

        price_per_unit = drink_prices.get(drink_option, 0)
        if price_per_unit == 0:
            return HttpResponse("Invalid coffee selection.")

        total_amount = price_per_unit * quantity
        amount_in_paise = total_amount * 100  # Razorpay expects amount in paise

        # Create Razorpay order
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        order = client.order.create({
            'amount': amount_in_paise,
            'currency': 'INR',
            'payment_capture': '1'
        })

        # Save the order details to the database
        coffee = Coffee(name=name, quantity=quantity, amount=total_amount, email=email, phone=phone_number, order_id=order['id'], drink_option=drink_option)
        coffee.save()

        # Send SMS with the invoice link after the order is placed
        send_sms_with_invoice(phone_number, order['id'], total_amount)

        # Render the order confirmation page
        return render(request, 'app1/home.html', {'order': order, 'quantity': quantity, 'price': total_amount})

    return render(request, 'app1/home.html')

# Success view to handle payment confirmation (Optional, depends on your Razorpay integration)
@csrf_exempt
def success_view(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        
        # Extract order ID from POST data
        for key, val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break

        # Retrieve the coffee object based on the order ID
        coffee = Coffee.objects.filter(order_id=order_id).first()
        
        if coffee is not None:
            # Mark the order as paid
            coffee.paid = True
            coffee.save()

            # Prepare email content
            msg_plain = render_to_string('app1/email.txt', {'coffee': coffee})
            msg_html = render_to_string('app1/email.html', {'coffee': coffee})
            recipient_email = coffee.email
            
            # Send email notification to the user
            send_mail('Your payment has been received',
                      msg_plain,
                      settings.EMAIL_HOST_USER,
                      [recipient_email],
                      html_message=msg_html)

            # Optionally render a success page
            return render(request, "app1/success.html")
        return HttpResponse("Order failed")

