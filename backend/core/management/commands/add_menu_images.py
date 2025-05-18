from django.core.management.base import BaseCommand
from core.models import MenuItem
import os
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.parse import urlparse

class Command(BaseCommand):
    help = 'Adds images to menu items'

    def handle(self, *args, **kwargs):
        # Dictionary mapping menu item names to image URLs
        image_urls = {
            # Breakfast items
            'Masala Dosa': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe',
            'Idli Sambar': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Poha': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Upma': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Medu Vada': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Aloo Paratha': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Puri Bhaji': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Dosa': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Uttapam': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Pongal': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Sabudana Khichdi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Besan Chilla': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Methi Thepla': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Rava Idli': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Mysore Bonda': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Rava Dosa': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Set Dosa': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Neer Dosa': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Appam': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Pesarattu': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Cheela': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Dhokla': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Khandvi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Patra': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Handvo': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',

            # Main Course items
            'Paneer Butter Masala': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Dal Makhani': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Palak Paneer': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Chana Masala': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Malai Kofta': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Rajma Masala': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Kadai Paneer': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Mushroom Masala': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Aloo Gobi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Baingan Bharta': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Navratan Korma': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Vegetable Biryani': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Paneer Tikka Masala': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Dal Tadka': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Jeera Aloo': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Bhindi Masala': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Aloo Matar': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Methi Malai Mutter': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Dum Aloo': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Paneer Do Pyaza': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Dal Fry': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Mix Vegetable': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Paneer Pasanda': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Dal Palak': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Aloo Jeera': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',

            # Breads
            'Butter Naan': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Garlic Naan': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Plain Naan': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Tandoori Roti': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Missi Roti': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Lachha Paratha': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Aloo Paratha': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Gobi Paratha': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Methi Paratha': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Pudina Paratha': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Ajwain Paratha': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Paneer Paratha': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Onion Kulcha': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Stuffed Kulcha': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Plain Kulcha': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Rumali Roti': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Tandoori Roti': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Phulka': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Bhatura': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Poori': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Thepla': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Bhakri': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Makki Roti': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Bajra Roti': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',

            # Snacks
            'Pani Puri': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Dahi Puri': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Bhel Puri': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Sev Puri': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Pav Bhaji': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Vada Pav': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Samosa': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Kachori': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Dhokla': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Khandvi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Patra': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Handvo': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Dabeli': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Misal Pav': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Poha': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Upma': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Idli': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Dosa': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Uttapam': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Medu Vada': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Sambar Vada': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Rasam Vada': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Curd Vada': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Bonda': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',

            # Desserts
            'Gulab Jamun': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Rasmalai': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Rasgulla': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Jalebi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Kheer': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Gajar Halwa': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Moong Dal Halwa': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Besan Ladoo': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Moti Choor Ladoo': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Coconut Ladoo': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Badam Halwa': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Shahi Tukda': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Phirni': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Malpua': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Rabri': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Kulfi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Falooda': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Mango Kulfi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Pista Kulfi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Malai Kulfi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Kaju Katli': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Mysore Pak': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Soan Papdi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Balushahi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Imarti': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',

            # Beverages
            'Masala Chai': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Ginger Tea': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Cardamom Tea': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Lemon Tea': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Mango Lassi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Sweet Lassi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Salted Lassi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Rose Lassi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Pista Lassi': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Badam Milk': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Kesar Milk': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Thandai': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Jaljeera': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Aam Panna': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Nimbu Pani': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Kokum Sherbet': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Sugarcane Juice': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Coconut Water': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Mango Shake': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Banana Shake': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Chikoo Shake': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Papaya Shake': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Strawberry Shake': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Pineapple Shake': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
            'Mixed Fruit Shake': 'https://images.unsplash.com/photo-1601050690597-df0568f70950',
        }

        for item_name, image_url in image_urls.items():
            try:
                menu_item = MenuItem.objects.get(name=item_name)
                if not menu_item.image:
                    # Download the image
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        # Create a temporary file
                        img_temp = NamedTemporaryFile(delete=True)
                        img_temp.write(response.content)
                        img_temp.flush()

                        # Get the file extension
                        file_ext = os.path.splitext(urlparse(image_url).path)[1]
                        if not file_ext:
                            file_ext = '.jpg'

                        # Save the image
                        menu_item.image.save(f"{item_name}{file_ext}", File(img_temp), save=True)
                        self.stdout.write(self.style.SUCCESS(f'Successfully added image for {item_name}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Failed to download image for {item_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Image already exists for {item_name}'))
            except MenuItem.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Menu item {item_name} not found'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {item_name}: {str(e)}')) 