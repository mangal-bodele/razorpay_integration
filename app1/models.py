from django.db import models

class Coffee(models.Model):
    razorpay_order_id = models.CharField(max_length=255, null=False, blank=False, default='Unknown')  # Default 'Unknown'
    amount = models.IntegerField(null=False, blank=False, default=0)  # Default value 0
    status = models.CharField(max_length=20, default='pending', null=False, blank=False)  # Default 'pending'
    name = models.CharField(max_length=100, null=False, blank=False, default='Anonymous')  # Default 'Anonymous'
    phone = models.CharField(max_length=15, null=True, blank=True, default='')  # Default empty string
    email = models.EmailField(null=True, blank=True, default='')  # Default empty string
    drink_option = models.CharField(max_length=50, null=True, blank=True, default='')  # Default empty string
    quantity = models.IntegerField(null=False, blank=False, default=1)  # Default value 1

    def __str__(self):
        return f"Order {self.razorpay_order_id} - {self.status}"
