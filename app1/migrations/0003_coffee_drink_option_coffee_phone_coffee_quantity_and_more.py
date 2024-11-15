# Generated by Django 5.0.2 on 2024-11-09 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_coffee_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='coffee',
            name='drink_option',
            field=models.CharField(default='Unknown', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='coffee',
            name='phone',
            field=models.CharField(default=None, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='coffee',
            name='quantity',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='email',
            field=models.EmailField(default=None, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='name',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='order_id',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
