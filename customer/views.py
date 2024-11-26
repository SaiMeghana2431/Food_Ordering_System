from django.shortcuts import get_object_or_404, render, redirect
from .forms import CustomerSignupForm
from django.contrib.auth import authenticate, login
from .models import Customer, CartItem, Order
from django.contrib import messages
from restaurant.models import Restaurant, MenuItem

def signup(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer:login')
    else:
        form = CustomerSignupForm()
    return render(request, 'customer/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('emailId')
        password = request.POST.get('password')
        
        try:
            customer = Customer.objects.get(emailId=email, password=password)
            request.session['user_id'] = customer.id  
            return redirect('customer:customer_home') 
        except Customer.DoesNotExist:
            return render(request, 'customer/login.html', {'error': 'Invalid credentials'})

    return render(request, 'customer/login.html')

def customer_home(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('customer:login')
    
    customer = Customer.objects.get(id=user_id)
    return render(request, 'customer/home.html', {'user': customer})

def about(request):
    return render(request, 'customer/about.html')

def food_items(request):
    restaurants = Restaurant.objects.all()  
    return render(request, 'customer/food_items.html', {'restaurants': restaurants})

def menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    
    return render(request, 'customer/menu.html', {'restaurant': restaurant, 'menu_items': menu_items})


def profile_view(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('customer:login') 
    
    customer = Customer.objects.get(id=user_id)
    
    return render(request, 'customer/profile.html', {'user': customer})

def profile_edit(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('customer:login') 
    
    customer = Customer.objects.get(id=user_id)

    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.street = request.POST.get('street')
        customer.city = request.POST.get('city')
        customer.pincode = request.POST.get('pincode')
        customer.description = request.POST.get('description')

        customer.save()

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('customer:profile')

    return render(request, 'customer/profile_edit.html', {'user': customer})

from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from customer.models import Customer, CartItem, MenuItem
import json

def add_to_cart(request):
    if request.method == "POST":
        customer_id = request.session.get('user_id')
        if not customer_id:
            return redirect('customer:login')  

        customer = get_object_or_404(Customer, id=customer_id)
        cart_data = request.POST.get('cart_data')

        if cart_data:
            cart_data = json.loads(cart_data)  

            for item in cart_data:
                item_id = item.get('item_id')
                quantity = item.get('quantity', 0)

                if quantity > 0:
                    menu_item = get_object_or_404(MenuItem, id=item_id)

                    cart_item, created = CartItem.objects.get_or_create(
                        customer=customer,
                        menu_item=menu_item,
                        defaults={'quantity': quantity}
                    )

                    if not created:
                        cart_item.quantity += quantity
                        cart_item.save()

            return redirect('customer:cart') 

    return redirect('customer:menu')


def cart_view(request):
    customer_id = request.session.get('user_id')
    if not customer_id:
        return redirect('customer:login') 
    
    customer = get_object_or_404(Customer, id=customer_id)
    
    cart_items = CartItem.objects.filter(customer=customer)

    if request.method == 'POST':
        if 'delete_item' in request.POST:
            delete_item_id = request.POST['delete_item']
            cart_item_to_delete = get_object_or_404(CartItem, id=delete_item_id)
            cart_item_to_delete.delete()

            cart_items = CartItem.objects.filter(customer=customer)

        for cart_item in cart_items:
            quantity_key = f'quantity_{cart_item.id}'
            
            if quantity_key in request.POST:
                new_quantity = int(request.POST[quantity_key])
                if new_quantity >= 1:
                    cart_item.quantity = new_quantity
                    cart_item.total_price = cart_item.menu_item.price * new_quantity 
                    cart_item.save()

            if 'increase' in request.POST and str(cart_item.id) == request.POST['increase']:
                cart_item.quantity += 1
                cart_item.total_price = cart_item.menu_item.price * cart_item.quantity  
                cart_item.save()

            if 'decrease' in request.POST and str(cart_item.id) == request.POST['decrease']:
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.total_price = cart_item.menu_item.price * cart_item.quantity 
                    cart_item.save()

        cart_items = CartItem.objects.filter(customer=customer)

        if 'place_order' in request.POST:
            if cart_items:
                restaurant = cart_items[0].menu_item.restaurant 
                ordered_items = []
                for cart_item in cart_items:
                    ordered_items.append({
                        'item_name': cart_item.menu_item.name,  
                        'item_id': cart_item.menu_item.id, 
                        'quantity': cart_item.quantity,  
                        'total_price': float(cart_item.total_price) 
                    })

                total_cost = sum(float(cart_item.total_price) for cart_item in cart_items) 

                order = Order.objects.create(
                    customer=customer,
                    restaurant=restaurant,
                    ordered_items=ordered_items,
                    total_cost=total_cost
                )

                CartItem.objects.filter(customer=customer).delete()

                messages.success(request, 'Your order has been placed successfully!')
                return redirect('customer:customer_home') 

    return render(request, 'customer/cart.html', {'cart_items': cart_items})

def ordered_items(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('customer:login') 

    customer = Customer.objects.get(id=user_id)

    orders = Order.objects.filter(customer=customer)

    order_data = []
    for order in orders:
        restaurant = order.restaurant  
        order_data.append({
            'order': order,
            'restaurant': restaurant
        })

    return render(request, 'customer/ordered_items.html', {'order_data': order_data})
