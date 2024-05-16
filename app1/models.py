from django.db import models

class Coffee(models.Model):
    name = models.CharField(max_length=30, null=True)
    amount = models.CharField(max_length=30, null=True)
    email = models.EmailField(null=True)
    order_id = models.CharField(max_length=30, null=True)
    paid = models.BooleanField(default=False)
