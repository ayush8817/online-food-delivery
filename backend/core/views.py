from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .forms import UserRegistrationForm, OrderForm
from .models import Restaurant, Category, MenuItem, Order, OrderItem
from decimal import Decimal
import json

def home(request):
    restaurants = Restaurant.objects.filter(is_active=True)
    featured_items = MenuItem.objects.filter(is_available=True).select_related('restaurant')[:6]
    return render(request, 'home.html', {
        'restaurants': restaurants,
        'featured_items': featured_items
    })

def menu(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    restaurant_id = request.GET.get('restaurant')
    
    menu_items = MenuItem.objects.filter(is_available=True).select_related('restaurant', 'category')
    categories = Category.objects.filter(is_active=True)
    restaurants = Restaurant.objects.filter(is_active=True)
    
    if query:
        menu_items = menu_items.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(restaurant__name__icontains=query)
        )
    
    if category_id:
        menu_items = menu_items.filter(category_id=category_id)
    
    if restaurant_id:
        menu_items = menu_items.filter(restaurant_id=restaurant_id)
        selected_restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    else:
        selected_restaurant = None
    
    return render(request, 'menu.html', {
        'menu_items': menu_items,
        'categories': categories,
        'restaurants': restaurants,
        'selected_category': category_id,
        'selected_restaurant': selected_restaurant,
        'search_query': query
    })

@login_required
def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Initialize cart if it doesn't exist
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    cart_items = request.session['cart']
    items = []
    subtotal = Decimal('0.00')
    discount_amount = Decimal('0.00')
    
    for item_id, quantity in cart_items.items():
        try:
            item = MenuItem.objects.get(id=item_id)
            total = item.price * Decimal(str(quantity))
            subtotal += total
            items.append({
                'item': item,
                'quantity': quantity,
                'total': total
            })
        except MenuItem.DoesNotExist:
            # Remove invalid items from cart
            del cart_items[item_id]
            request.session['cart'] = cart_items
            request.session.modified = True
            continue
    
    # Calculate tax and total
    tax = subtotal * Decimal('0.05')  # 5% tax
    total = subtotal + tax - discount_amount
    
    # Handle coupon code
    current_coupon = None
    if items and items[0]['item'].restaurant:
        current_coupon = items[0]['item'].restaurant.coupon_code
    
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        if coupon_code and items:
            try:
                restaurant = items[0]['item'].restaurant
                if restaurant and restaurant.coupon_code == coupon_code:
                    discount_amount = subtotal * (restaurant.discount_percentage / Decimal('100'))
                    total = subtotal + tax - discount_amount
                    messages.success(request, f'Coupon applied! You saved ₹{discount_amount:.2f}')
                else:
                    messages.error(request, 'Invalid coupon code')
            except Exception as e:
                messages.error(request, 'Error applying coupon code')
    
    context = {
        'items': items,
        'subtotal': subtotal,
        'tax': tax,
        'discount_amount': discount_amount,
        'total': total,
        'current_coupon': current_coupon
    }
    return render(request, 'cart.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def order_confirmation(request):
    return render(request, 'order_confirmation.html')

@csrf_exempt
@require_POST
def update_cart(request):
    if request.method == 'POST':
        try:
            item_id = request.POST.get('item_id')
            action = request.POST.get('action')
            
            if not item_id:
                return JsonResponse({'status': 'error', 'message': 'Item ID is required'})
            
            try:
                menu_item = MenuItem.objects.get(id=item_id)
            except MenuItem.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Item not found'})
            
            # Initialize cart if it doesn't exist
            if 'cart' not in request.session:
                request.session['cart'] = {}
            
            cart = request.session['cart']
            
            if action == 'add':
                cart[item_id] = cart.get(item_id, 0) + 1
            elif action == 'remove':
                if item_id in cart:
                    if cart[item_id] > 1:
                        cart[item_id] -= 1
                    else:
                        del cart[item_id]
            elif action == 'delete':
                cart.pop(item_id, None)
            
            # Save the cart back to session
            request.session['cart'] = cart
            request.session.modified = True
            
            # Calculate total items in cart
            cart_count = sum(cart.values())
            
            return JsonResponse({
                'status': 'success',
                'cart_count': cart_count,
                'message': 'Cart updated successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error updating cart: {str(e)}'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('cart')
        
        form = OrderForm(request.POST)
        if form.is_valid():
            delivery_address = form.cleaned_data['delivery_address']
            delivery_phone = form.cleaned_data['delivery_phone']
            payment_method = form.cleaned_data['payment_method']
            
            # Get the first restaurant from the cart items
            first_item = MenuItem.objects.get(id=list(cart.keys())[0])
            restaurant = first_item.restaurant
            
            # Calculate discount if valid coupon
            discount_amount = Decimal('0')
            coupon_code = request.POST.get('coupon_code')
            if coupon_code and restaurant.coupon_code == coupon_code:
                subtotal = sum(MenuItem.objects.get(id=item_id).price * Decimal(str(quantity))
                             for item_id, quantity in cart.items())
                discount_amount = subtotal * (restaurant.discount_percentage / Decimal('100'))
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                restaurant=restaurant,
                delivery_address=delivery_address,
                delivery_phone=delivery_phone,
                payment_method=payment_method,
                total_amount=0,
                coupon_code=coupon_code,
                discount_amount=discount_amount
            )
            
            # Create order items and calculate total
            total = Decimal('0')
            for item_id, quantity in cart.items():
                menu_item = MenuItem.objects.get(id=item_id)
                price = menu_item.price * Decimal(str(quantity))
                total += price
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price=price
                )
            
            # Update order total
            order.total_amount = total - discount_amount
            order.save()
            
            # Clear cart
            request.session['cart'] = {}
            
            return redirect('order_detail', order_id=order.id)
        else:
            messages.error(request, 'Please fill in all required fields correctly.')
            return redirect('cart')
    
    return redirect('cart')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order}) 