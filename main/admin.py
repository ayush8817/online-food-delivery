from django.contrib import admin
from .models import Category, MenuItem, Order  # Added Order here

# Register the models so they appear in the admin panel
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)  # Registering the Order model

