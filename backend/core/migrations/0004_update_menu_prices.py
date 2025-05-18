from django.db import migrations
from decimal import Decimal

def update_prices(apps, schema_editor):
    MenuItem = apps.get_model('core', 'MenuItem')
    
    # Update prices for all menu items
    for item in MenuItem.objects.all():
        # Only adjust prices that are outside the range
        if item.price < Decimal('150.00'):
            item.price = Decimal('150.00')
        elif item.price > Decimal('300.00'):
            item.price = Decimal('300.00')
        # Prices between 150 and 300 remain unchanged
        item.save()

def reverse_prices(apps, schema_editor):
    # This is a no-op since we can't know the original prices
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_add_restaurants'),
    ]

    operations = [
        migrations.RunPython(update_prices, reverse_prices),
    ] 