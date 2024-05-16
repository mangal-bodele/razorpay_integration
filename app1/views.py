from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
import razorpay
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .models import Coffee

def home_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount_str = request.POST.get('amount')
        amount = int(float(amount_str) * 100)
        email = request.POST.get('email')
        client = razorpay.Client(auth=("rzp_test_QgB83gVHMMYucR", "3z3erDw3yTT0YOkwDY6zOCHb"))
        order = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        coffee = Coffee(name=name, amount=amount, email=email, order_id=order['id'])
        coffee.save()
        return render(request, 'app1/home.html', {'order': order})

    return render(request, 'app1/home.html')


@csrf_exempt
def success_view(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        for key, val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break

        coffee = Coffee.objects.filter(order_id=order_id).first()
        if coffee is not None:
            coffee.paid = True
            coffee.save()

            msg_plain = render_to_string('app1/email.txt')
            msg_html = render_to_string('app1/email.html')
            reciepient_email =coffee.email
            send_mail('Your payment has been received',
                        msg_plain,
                        settings.EMAIL_HOST_USER,
                        [reciepient_email],
                        html_message=msg_html)

            return render(request, "app1/success.html")
        return HttpResponse("order failed")

