import razorpay
from django.conf import settings

# Razorpay client initialization
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def verify_payment_signature(payment_id, order_id, signature):
    """
    Verify Razorpay payment signature.
    """
    try:
        # Razorpay signature verification
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        client.utility.verify_payment_signature(params_dict)
        return True
    except razorpay.errors.SignatureVerificationError:
        return False
