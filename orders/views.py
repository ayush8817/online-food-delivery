from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import MenuItem, Category, Order, OrderItem
from .forms import UserRegistrationForm, OrderForm
from decimal import Decimal



@login_required
def cart(request):
    cart_items = []
    total_amount = Decimal('0.00')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total_amount
            order.save()
            
            # Process cart items from session
            cart_items = request.session.get('cart', [])
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item_id=item['id'],
                    quantity=item['quantity']
                )
            
            # Clear cart
            request.session['cart'] = []
            messages.success(request, 'Order placed successfully!')
            return redirect('order_confirmation')
    else:
        form = OrderForm()
        
        # Calculate cart total
        cart_items = request.session.get('cart', [])
        for item in cart_items:
            menu_item = MenuItem.objects.get(id=item['id'])
            item_total = menu_item.price * item['quantity']
            total_amount += item_total
            cart_items[cart_items.index(item)]['name'] = menu_item.name
            cart_items[cart_items.index(item)]['price'] = menu_item.price
            cart_items[cart_items.index(item)]['total'] = item_total
    
    return render(request, 'cart.html', {
        'form': form,
        'cart_items': cart_items,
        'total_amount': total_amount
    })

