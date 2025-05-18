from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('place-order/', views.place_order, name='place_order'),
    # Add other routes like login/register/profile if they are in this app
]
