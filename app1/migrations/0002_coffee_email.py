# Generated by Django 5.0.6 on 2024-05-11 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coffee',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]