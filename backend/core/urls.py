from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('register/', views.register, name='register'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
] 