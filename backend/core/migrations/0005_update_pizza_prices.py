from django.db import migrations
from decimal import Decimal

def update_pizza_prices(apps, schema_editor):
    MenuItem = apps.get_model('core', 'MenuItem')
    Category = apps.get_model('core', 'Category')
    
    # Get or create the pizza category
    pizza_category, created = Category.objects.get_or_create(
        name='Pizza',
        defaults={
            'description': 'Delicious pizzas with various toppings',
            'is_active': True
        }
    )
    
    # Update prices for all pizza items
    for item in MenuItem.objects.filter(category=pizza_category):
        # Only adjust prices that are outside the range
        if item.price < Decimal('200.00'):
            item.price = Decimal('200.00')
        elif item.price > Decimal('350.00'):
            item.price = Decimal('350.00')
        # Prices between 200 and 350 remain unchanged
        item.save()

def reverse_pizza_prices(apps, schema_editor):
    # This is a no-op since we can't know the original prices
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_update_menu_prices'),
    ]

    operations = [
        migrations.RunPython(update_pizza_prices, reverse_pizza_prices),
    ] 