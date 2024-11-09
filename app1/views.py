import json
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
from io import BytesIO
from reportlab.pdfgen import canvas # type: ignore
from .models import Coffee
from .utils import verify_payment_signature
from twilio.rest import Client # type: ignore
from twilio.base.exceptions import TwilioRestException # type: ignore


# Razorpay Client Initialization
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def home_view(request):
    razorpay_key = settings.RAZORPAY_KEY_ID
    return render(request, 'app1/home.html', {'razorpay_key': razorpay_key})

def create_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            if not all(field in data for field in ['name', 'phone', 'email', 'drink_option', 'quantity']):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            drink_prices = {
                "espresso": 100,
                "latte": 150,
                "cappuccino": 120,
                "americano": 130,
                "mocha": 160,
                "flat_white": 170,
                "macchiato": 180,
                "cold_brew": 200
            }

            drink_option = data['drink_option']
            quantity = int(data['quantity'])
            amount = drink_prices.get(drink_option, 0) * quantity * 100

            if amount < 100:
                return JsonResponse({"error": "Order amount is too small"}, status=400)

            payment_order = razorpay_client.order.create(dict(amount=amount, currency="INR", payment_capture="1"))
            order_id = payment_order.get("id")

            Coffee.objects.create(
                razorpay_order_id=order_id,
                amount=amount,
                status='pending',
                name=data['name'],
                phone=data['phone'],
                email=data['email'],
                drink_option=drink_option,
                quantity=quantity
            )

            return JsonResponse({"order_id": order_id, "amount": amount, "currency": "INR"})
        
        except Exception as e:
            print(f"Error creating order: {e}")
            return JsonResponse({"error": "Error creating order"}, status=500)




def success_view(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        # Verify the payment
        if not verify_payment_signature(razorpay_payment_id, razorpay_order_id, razorpay_signature):
            return JsonResponse({"error": "Payment verification failed"}, status=400)

        try:
            # Find the coffee order using the order ID
            coffee_order = Coffee.objects.get(razorpay_order_id=razorpay_order_id)
            coffee_order.status = 'paid'  # Update status to 'paid'
            coffee_order.save()

            # Send a confirmation email to the customer
            send_mail(
                'Order Confirmation - Coffee Shop',
                f'Thank you for your order! Your payment was successful. Order ID: {razorpay_order_id}',
                'no-reply@coffeeshop.com',
                [coffee_order.email],  # Send the email to the customer
                fail_silently=False,
            )

            return redirect('success')  # Redirect to the success page after payment is processed

        except Coffee.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)

    elif request.method == 'GET':
        return render(request, 'app1/success.html')  # Show the success page

    return JsonResponse({"error": "Invalid method. Expected POST or GET."}, status=405)



def send_sms(phone_number, message):
    
    try:
        # Initialize Twilio client using settings
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # Send the message
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        print(f"Message sent to {phone_number}")
    
    except TwilioRestException as e:
        print(f"Error occurred while sending SMS: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")


def generate_invoice(amount, transaction_id):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, f"Invoice ID: {transaction_id}")
    c.drawString(100, 730, f"Amount: {amount} INR")
    c.save()
    buffer.seek(0)
    return buffer

def send_email_with_invoice(email, amount, transaction_id):
    pdf = generate_invoice(amount, transaction_id)
    email_subject = "Your Payment Invoice"
    email_body = f"Thank you for your payment of {amount} INR. Please find your invoice attached."
    
    email_message = EmailMessage(email_subject, email_body, 'from@example.com', [email])
    email_message.attach(f"Invoice_{transaction_id}.pdf", pdf.read(), 'application/pdf')
    email_message.send()

def on_payment_success(user_phone, user_email, amount, transaction_id):
    message = f"Thank you for your payment of {amount} INR. Your transaction ID is {transaction_id}."
    send_sms(user_phone, message)
    send_email_with_invoice(user_email, amount, transaction_id)

on_payment_success('+919876543210', 'user@example.com', 500, 'TX12345')
