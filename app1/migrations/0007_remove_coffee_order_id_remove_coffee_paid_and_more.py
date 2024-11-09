# Generated by Django 5.0.2 on 2024-11-09 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_alter_coffee_amount_alter_coffee_drink_option_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coffee',
            name='order_id',
        ),
        migrations.RemoveField(
            model_name='coffee',
            name='paid',
        ),
        migrations.AddField(
            model_name='coffee',
            name='razorpay_order_id',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AddField(
            model_name='coffee',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='drink_option',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='name',
            field=models.CharField(default='Anonymous', max_length=100),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
