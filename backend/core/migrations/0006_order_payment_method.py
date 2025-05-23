# Generated by Django 4.2.7 on 2025-04-18 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_update_pizza_prices'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash on Delivery'), ('card', 'Credit/Debit Card'), ('upi', 'UPI Payment')], default='cash', max_length=20),
        ),
    ]
