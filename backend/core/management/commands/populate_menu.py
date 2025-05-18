from django.core.management.base import BaseCommand
from core.models import Category, MenuItem
from django.core.files import File
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Populates the database with food categories and menu items'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = {
            'Breakfast': {
                'description': 'Start your day with our delicious Indian breakfast options',
                'items': [
                    {'name': 'Masala Dosa', 'description': 'Crispy rice crepe with spiced potato filling', 'price': 120},
                    {'name': 'Idli Sambar', 'description': 'Steamed rice cakes with lentil soup', 'price': 80},
                    {'name': 'Poha', 'description': 'Flattened rice with vegetables and spices', 'price': 70},
                    {'name': 'Upma', 'description': 'Semolina cooked with vegetables and spices', 'price': 60},
                    {'name': 'Medu Vada', 'description': 'Crispy lentil doughnuts with coconut chutney', 'price': 90},
                    {'name': 'Aloo Paratha', 'description': 'Stuffed potato flatbread with curd', 'price': 100},
                    {'name': 'Puri Bhaji', 'description': 'Deep-fried bread with potato curry', 'price': 110},
                    {'name': 'Mysore Bonda', 'description': 'Spiced lentil fritters', 'price': 80},
                    {'name': 'Rava Idli', 'description': 'Semolina steamed cakes', 'price': 85},
                    {'name': 'Besan Chilla', 'description': 'Gram flour pancakes with vegetables', 'price': 75},
                    {'name': 'Sabudana Khichdi', 'description': 'Tapioca pearls with peanuts and spices', 'price': 95},
                    {'name': 'Methi Thepla', 'description': 'Fenugreek flatbread', 'price': 90},
                    {'name': 'Dahi Vada', 'description': 'Lentil dumplings in yogurt', 'price': 100},
                    {'name': 'Rava Dosa', 'description': 'Crispy semolina crepe', 'price': 110},
                    {'name': 'Set Dosa', 'description': 'Soft, spongy rice pancakes', 'price': 95},
                    {'name': 'Khaman Dhokla', 'description': 'Steamed gram flour cake', 'price': 85},
                    {'name': 'Methi Paratha', 'description': 'Fenugreek stuffed flatbread', 'price': 90},
                    {'name': 'Pongal', 'description': 'Rice and lentil porridge with ghee', 'price': 80},
                    {'name': 'Bread Upma', 'description': 'Bread cooked with vegetables and spices', 'price': 70},
                    {'name': 'Mangalore Buns', 'description': 'Sweet banana bread', 'price': 85},
                    {'name': 'Neer Dosa', 'description': 'Thin rice crepes', 'price': 90},
                    {'name': 'Kanda Poha', 'description': 'Flattened rice with onions and spices', 'price': 75},
                    {'name': 'Ragi Dosa', 'description': 'Finger millet crepes', 'price': 100},
                    {'name': 'Moong Dal Chilla', 'description': 'Mung bean pancakes', 'price': 80},
                    {'name': 'Sabudana Vada', 'description': 'Tapioca pearl fritters', 'price': 90},
                ]
            },
            'Main Course': {
                'description': 'Traditional Indian vegetarian main course dishes',
                'items': [
                    {'name': 'Paneer Butter Masala', 'description': 'Cottage cheese in rich tomato gravy', 'price': 220},
                    {'name': 'Dal Makhani', 'description': 'Creamy black lentils cooked with butter', 'price': 180},
                    {'name': 'Vegetable Biryani', 'description': 'Fragrant rice with mixed vegetables', 'price': 200},
                    {'name': 'Palak Paneer', 'description': 'Cottage cheese in spinach gravy', 'price': 210},
                    {'name': 'Chana Masala', 'description': 'Chickpeas in spicy tomato gravy', 'price': 190},
                    {'name': 'Malai Kofta', 'description': 'Vegetable dumplings in creamy gravy', 'price': 230},
                    {'name': 'Rajma Masala', 'description': 'Kidney beans in spicy gravy', 'price': 190},
                    {'name': 'Mushroom Masala', 'description': 'Mushrooms in rich tomato gravy', 'price': 200},
                    {'name': 'Baingan Bharta', 'description': 'Smoked eggplant curry', 'price': 180},
                    {'name': 'Aloo Gobi', 'description': 'Potato and cauliflower curry', 'price': 170},
                    {'name': 'Methi Malai Mutter', 'description': 'Fenugreek leaves with peas in cream', 'price': 200},
                    {'name': 'Kadai Paneer', 'description': 'Cottage cheese in bell pepper gravy', 'price': 220},
                    {'name': 'Navratan Korma', 'description': 'Mixed vegetables in creamy gravy', 'price': 210},
                    {'name': 'Jeera Aloo', 'description': 'Potatoes tempered with cumin', 'price': 160},
                    {'name': 'Dum Aloo', 'description': 'Baby potatoes in spicy gravy', 'price': 190},
                    {'name': 'Bhindi Masala', 'description': 'Okra cooked with spices', 'price': 170},
                    {'name': 'Lauki Kofta', 'description': 'Bottle gourd dumplings in gravy', 'price': 200},
                    {'name': 'Mushroom Do Pyaza', 'description': 'Mushrooms with double onions', 'price': 210},
                    {'name': 'Aloo Jeera', 'description': 'Potatoes with cumin seeds', 'price': 160},
                    {'name': 'Methi Matar Malai', 'description': 'Fenugreek leaves with peas in cream', 'price': 200},
                    {'name': 'Kaju Curry', 'description': 'Cashew nuts in rich gravy', 'price': 240},
                    {'name': 'Vegetable Jalfrezi', 'description': 'Mixed vegetables in spicy gravy', 'price': 190},
                    {'name': 'Aloo Matar', 'description': 'Potatoes with green peas', 'price': 170},
                    {'name': 'Mushroom Masala', 'description': 'Mushrooms in spicy gravy', 'price': 200},
                    {'name': 'Paneer Tikka Masala', 'description': 'Grilled cottage cheese in gravy', 'price': 230},
                ]
            },
            'Breads': {
                'description': 'Freshly made Indian breads',
                'items': [
                    {'name': 'Naan', 'description': 'Soft leavened bread', 'price': 50},
                    {'name': 'Roti', 'description': 'Whole wheat flatbread', 'price': 30},
                    {'name': 'Paratha', 'description': 'Layered flatbread with ghee', 'price': 60},
                    {'name': 'Butter Naan', 'description': 'Naan brushed with butter', 'price': 70},
                    {'name': 'Garlic Naan', 'description': 'Naan with garlic and butter', 'price': 80},
                    {'name': 'Missi Roti', 'description': 'Spiced gram flour bread', 'price': 50},
                    {'name': 'Tandoori Roti', 'description': 'Whole wheat bread cooked in tandoor', 'price': 40},
                    {'name': 'Lachha Paratha', 'description': 'Layered flaky bread', 'price': 70},
                    {'name': 'Stuffed Paratha', 'description': 'Stuffed flatbread with various fillings', 'price': 90},
                    {'name': 'Roomali Roti', 'description': 'Thin handkerchief bread', 'price': 45},
                    {'name': 'Bhatura', 'description': 'Deep-fried leavened bread', 'price': 60},
                    {'name': 'Kulcha', 'description': 'Leavened bread with various toppings', 'price': 70},
                    {'name': 'Puri', 'description': 'Deep-fried puffed bread', 'price': 40},
                    {'name': 'Phulka', 'description': 'Thin whole wheat bread', 'price': 35},
                    {'name': 'Makki ki Roti', 'description': 'Corn flour bread', 'price': 50},
                    {'name': 'Bajra Roti', 'description': 'Pearl millet bread', 'price': 50},
                    {'name': 'Jowar Roti', 'description': 'Sorghum bread', 'price': 50},
                    {'name': 'Ragi Roti', 'description': 'Finger millet bread', 'price': 55},
                    {'name': 'Thepla', 'description': 'Spiced flatbread', 'price': 60},
                    {'name': 'Pudina Paratha', 'description': 'Mint flavored flatbread', 'price': 70},
                    {'name': 'Aloo Paratha', 'description': 'Potato stuffed flatbread', 'price': 80},
                    {'name': 'Gobi Paratha', 'description': 'Cauliflower stuffed flatbread', 'price': 80},
                    {'name': 'Paneer Paratha', 'description': 'Cottage cheese stuffed flatbread', 'price': 90},
                    {'name': 'Methi Paratha', 'description': 'Fenugreek flavored flatbread', 'price': 70},
                    {'name': 'Onion Kulcha', 'description': 'Leavened bread with onions', 'price': 80},
                ]
            },
            'Snacks': {
                'description': 'Popular Indian vegetarian snacks',
                'items': [
                    {'name': 'Samosa', 'description': 'Crispy pastry with spiced potato filling', 'price': 40},
                    {'name': 'Pani Puri', 'description': 'Crisp puris with tangy water and fillings', 'price': 50},
                    {'name': 'Bhel Puri', 'description': 'Puffed rice with chutneys and vegetables', 'price': 60},
                    {'name': 'Dahi Puri', 'description': 'Crisp puris with yogurt and chutneys', 'price': 60},
                    {'name': 'Sev Puri', 'description': 'Crisp puris with sev and chutneys', 'price': 55},
                    {'name': 'Pav Bhaji', 'description': 'Spiced vegetable mash with bread', 'price': 120},
                    {'name': 'Vada Pav', 'description': 'Spicy potato fritter in bread', 'price': 50},
                    {'name': 'Dahi Vada', 'description': 'Lentil dumplings in yogurt', 'price': 80},
                    {'name': 'Aloo Tikki', 'description': 'Spiced potato patties', 'price': 60},
                    {'name': 'Kachori', 'description': 'Deep-fried pastry with various fillings', 'price': 45},
                    {'name': 'Dhokla', 'description': 'Steamed gram flour cake', 'price': 70},
                    {'name': 'Khandvi', 'description': 'Gram flour rolls with coconut', 'price': 80},
                    {'name': 'Methi Muthia', 'description': 'Steamed fenugreek dumplings', 'price': 70},
                    {'name': 'Sabudana Vada', 'description': 'Tapioca pearl fritters', 'price': 60},
                    {'name': 'Corn Bhel', 'description': 'Corn with spices and chutneys', 'price': 65},
                    {'name': 'Ragda Pattice', 'description': 'Potato patties with white peas curry', 'price': 90},
                    {'name': 'Mysore Bonda', 'description': 'Spiced lentil fritters', 'price': 50},
                    {'name': 'Medu Vada', 'description': 'Lentil doughnuts', 'price': 60},
                    {'name': 'Poha', 'description': 'Flattened rice with vegetables', 'price': 50},
                    {'name': 'Upma', 'description': 'Semolina with vegetables', 'price': 50},
                    {'name': 'Idli', 'description': 'Steamed rice cakes', 'price': 60},
                    {'name': 'Dosa', 'description': 'Rice crepes with various fillings', 'price': 80},
                    {'name': 'Uttapam', 'description': 'Thick rice pancake with toppings', 'price': 70},
                    {'name': 'Masala Dosa', 'description': 'Rice crepe with potato filling', 'price': 90},
                    {'name': 'Rava Dosa', 'description': 'Semolina crepe', 'price': 80},
                ]
            },
            'Desserts': {
                'description': 'Traditional Indian sweets',
                'items': [
                    {'name': 'Gulab Jamun', 'description': 'Sweet milk dumplings in sugar syrup', 'price': 60},
                    {'name': 'Rasmalai', 'description': 'Soft cheese patties in sweetened milk', 'price': 80},
                    {'name': 'Kheer', 'description': 'Rice pudding with nuts and saffron', 'price': 70},
                    {'name': 'Gajar Halwa', 'description': 'Carrot pudding with nuts', 'price': 90},
                    {'name': 'Rasgulla', 'description': 'Spongy cheese balls in sugar syrup', 'price': 60},
                    {'name': 'Jalebi', 'description': 'Crispy spiral sweet in sugar syrup', 'price': 50},
                    {'name': 'Malpua', 'description': 'Sweet pancakes with rabri', 'price': 70},
                    {'name': 'Shahi Tukda', 'description': 'Bread pudding with rabri', 'price': 80},
                    {'name': 'Mysore Pak', 'description': 'Gram flour sweet with ghee', 'price': 60},
                    {'name': 'Besan Ladoo', 'description': 'Gram flour sweet balls', 'price': 50},
                    {'name': 'Moong Dal Halwa', 'description': 'Yellow lentil pudding', 'price': 90},
                    {'name': 'Badam Halwa', 'description': 'Almond pudding', 'price': 100},
                    {'name': 'Kaju Katli', 'description': 'Cashew fudge', 'price': 80},
                    {'name': 'Peda', 'description': 'Milk sweet with cardamom', 'price': 60},
                    {'name': 'Sandesh', 'description': 'Cottage cheese sweet', 'price': 70},
                    {'name': 'Rabri', 'description': 'Sweetened condensed milk', 'price': 80},
                    {'name': 'Phirni', 'description': 'Ground rice pudding', 'price': 70},
                    {'name': 'Balushahi', 'description': 'Flaky sweet pastry', 'price': 60},
                    {'name': 'Imarti', 'description': 'Lentil flour sweet', 'price': 50},
                    {'name': 'Cham Cham', 'description': 'Cylindrical sweet with coconut', 'price': 70},
                    {'name': 'Malai Sandwich', 'description': 'Sweet sandwich with cream', 'price': 80},
                    {'name': 'Kulfi', 'description': 'Indian ice cream', 'price': 60},
                    {'name': 'Falooda', 'description': 'Vermicelli dessert with ice cream', 'price': 90},
                    {'name': 'Shrikhand', 'description': 'Sweetened strained yogurt', 'price': 70},
                    {'name': 'Mango Shrikhand', 'description': 'Sweetened yogurt with mango', 'price': 80},
                ]
            },
            'Beverages': {
                'description': 'Refreshing Indian drinks',
                'items': [
                    {'name': 'Masala Chai', 'description': 'Spiced Indian tea', 'price': 40},
                    {'name': 'Lassi', 'description': 'Sweet yogurt drink', 'price': 50},
                    {'name': 'Nimbu Pani', 'description': 'Fresh lemonade with spices', 'price': 40},
                    {'name': 'Mango Lassi', 'description': 'Sweet yogurt drink with mango', 'price': 60},
                    {'name': 'Rose Lassi', 'description': 'Sweet yogurt drink with rose', 'price': 55},
                    {'name': 'Salted Lassi', 'description': 'Salted yogurt drink', 'price': 50},
                    {'name': 'Badam Milk', 'description': 'Almond milk with saffron', 'price': 70},
                    {'name': 'Thandai', 'description': 'Spiced milk with nuts', 'price': 60},
                    {'name': 'Jaljeera', 'description': 'Spiced cumin water', 'price': 45},
                    {'name': 'Aam Panna', 'description': 'Raw mango drink', 'price': 50},
                    {'name': 'Kokum Sherbet', 'description': 'Kokum fruit drink', 'price': 45},
                    {'name': 'Sugarcane Juice', 'description': 'Fresh sugarcane juice', 'price': 40},
                    {'name': 'Coconut Water', 'description': 'Fresh tender coconut water', 'price': 50},
                    {'name': 'Mango Shake', 'description': 'Mango milkshake', 'price': 70},
                    {'name': 'Banana Shake', 'description': 'Banana milkshake', 'price': 60},
                    {'name': 'Strawberry Shake', 'description': 'Strawberry milkshake', 'price': 70},
                    {'name': 'Chocolate Shake', 'description': 'Chocolate milkshake', 'price': 65},
                    {'name': 'Vanilla Shake', 'description': 'Vanilla milkshake', 'price': 60},
                    {'name': 'Cold Coffee', 'description': 'Iced coffee with milk', 'price': 70},
                    {'name': 'Hot Chocolate', 'description': 'Hot chocolate drink', 'price': 65},
                    {'name': 'Green Tea', 'description': 'Hot green tea', 'price': 45},
                    {'name': 'Herbal Tea', 'description': 'Hot herbal tea', 'price': 50},
                    {'name': 'Ginger Tea', 'description': 'Hot ginger tea', 'price': 45},
                    {'name': 'Tulsi Tea', 'description': 'Hot holy basil tea', 'price': 50},
                    {'name': 'Masala Milk', 'description': 'Spiced hot milk', 'price': 55},
                ]
            }
        }

        # Create media directory if it doesn't exist
        media_dir = os.path.join(settings.MEDIA_ROOT, 'menu_images')
        os.makedirs(media_dir, exist_ok=True)

        # Create categories and menu items
        for category_name, category_data in categories.items():
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'description': category_data['description']}
            )
            
            self.stdout.write(self.style.SUCCESS(f'Created category: {category_name}'))
            
            for item_data in category_data['items']:
                menu_item, created = MenuItem.objects.get_or_create(
                    name=item_data['name'],
                    category=category,
                    defaults={
                        'description': item_data['description'],
                        'price': item_data['price'],
                        'is_available': True
                    }
                )
                
                self.stdout.write(self.style.SUCCESS(f'Created menu item: {item_data["name"]}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated the menu!')) 