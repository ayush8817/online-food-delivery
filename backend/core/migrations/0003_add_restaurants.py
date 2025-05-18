from django.db import migrations
from decimal import Decimal

def add_restaurants(apps, schema_editor):
    Restaurant = apps.get_model('core', 'Restaurant')
    Category = apps.get_model('core', 'Category')
    MenuItem = apps.get_model('core', 'MenuItem')

    # Create categories
    categories = {
        'North Indian': Category.objects.create(name='North Indian', is_active=True),
        'South Indian': Category.objects.create(name='South Indian', is_active=True),
        'Chinese': Category.objects.create(name='Chinese', is_active=True),
        'Street Food': Category.objects.create(name='Street Food', is_active=True),
        'Biryani': Category.objects.create(name='Biryani', is_active=True),
        'Desserts': Category.objects.create(name='Desserts', is_active=True),
    }

    # Create restaurants
    restaurants = {
        'Paradise Biryani': Restaurant.objects.create(
            name='Paradise Biryani',
            description='Famous for its authentic Hyderabadi biryani',
            address='123 Food Street, Hyderabad',
            phone='+91 9876543210',
            rating=4.5,
            is_active=True,
            coupon_code='PARADISE10',
            discount_percentage=Decimal('10.00')
        ),
        'Saravana Bhavan': Restaurant.objects.create(
            name='Saravana Bhavan',
            description='Authentic South Indian vegetarian cuisine',
            address='456 Temple Road, Chennai',
            phone='+91 9876543211',
            rating=4.3,
            is_active=True,
            coupon_code='SARAVANA15',
            discount_percentage=Decimal('15.00')
        ),
        'Haldiram\'s': Restaurant.objects.create(
            name='Haldiram\'s',
            description='Popular for North Indian snacks and sweets',
            address='789 Market Street, Delhi',
            phone='+91 9876543212',
            rating=4.2,
            is_active=True,
            coupon_code='HALDIRAM20',
            discount_percentage=Decimal('20.00')
        ),
        'Mainland China': Restaurant.objects.create(
            name='Mainland China',
            description='Contemporary Chinese cuisine',
            address='321 Business Park, Mumbai',
            phone='+91 9876543213',
            rating=4.4,
            is_active=True,
            coupon_code='CHINA25',
            discount_percentage=Decimal('25.00')
        ),
    }

    # Create menu items
    menu_items = [
        # Paradise Biryani
        {
            'restaurant': restaurants['Paradise Biryani'],
            'category': categories['Biryani'],
            'name': 'Hyderabadi Chicken Biryani',
            'description': 'Famous Hyderabadi biryani with tender chicken pieces',
            'price': Decimal('299.00'),
            'is_available': True
        },
        {
            'restaurant': restaurants['Paradise Biryani'],
            'category': categories['Biryani'],
            'name': 'Mutton Biryani',
            'description': 'Rich and flavorful mutton biryani',
            'price': Decimal('399.00'),
            'is_available': True
        },
        # Saravana Bhavan
        {
            'restaurant': restaurants['Saravana Bhavan'],
            'category': categories['South Indian'],
            'name': 'Masala Dosa',
            'description': 'Crispy dosa with potato masala filling',
            'price': Decimal('120.00'),
            'is_available': True
        },
        {
            'restaurant': restaurants['Saravana Bhavan'],
            'category': categories['South Indian'],
            'name': 'Idli Sambar',
            'description': 'Soft idlis with tangy sambar',
            'price': Decimal('80.00'),
            'is_available': True
        },
        # Haldiram's
        {
            'restaurant': restaurants['Haldiram\'s'],
            'category': categories['Street Food'],
            'name': 'Pani Puri',
            'description': 'Crispy puris with spicy water and chutneys',
            'price': Decimal('60.00'),
            'is_available': True
        },
        {
            'restaurant': restaurants['Haldiram\'s'],
            'category': categories['Desserts'],
            'name': 'Gulab Jamun',
            'description': 'Sweet milk-based dessert in sugar syrup',
            'price': Decimal('50.00'),
            'is_available': True
        },
        # Mainland China
        {
            'restaurant': restaurants['Mainland China'],
            'category': categories['Chinese'],
            'name': 'Hakka Noodles',
            'description': 'Stir-fried noodles with vegetables',
            'price': Decimal('180.00'),
            'is_available': True
        },
        {
            'restaurant': restaurants['Mainland China'],
            'category': categories['Chinese'],
            'name': 'Szechuan Chicken',
            'description': 'Spicy chicken with Szechuan sauce',
            'price': Decimal('250.00'),
            'is_available': True
        },
    ]

    for item in menu_items:
        MenuItem.objects.create(**item)

def remove_restaurants(apps, schema_editor):
    Restaurant = apps.get_model('core', 'Restaurant')
    Category = apps.get_model('core', 'Category')
    MenuItem = apps.get_model('core', 'MenuItem')

    MenuItem.objects.all().delete()
    Restaurant.objects.all().delete()
    Category.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_restaurant_remove_order_items_category_image_and_more'),
    ]

    operations = [
        migrations.RunPython(add_restaurants, remove_restaurants),
    ] 