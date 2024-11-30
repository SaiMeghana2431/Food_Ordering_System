from django.shortcuts import render, redirect,  get_object_or_404
from django.http import Http404

from customer.models import Order, Customer
from .forms import RestaurantSignupForm, MenuItemForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Restaurant, MenuItem

def signup(request):
    if request.method == 'POST':
        form = RestaurantSignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('restaurant:login')
    else:
        form = RestaurantSignupForm()
    return render(request, 'restaurant/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('emailId')
        password = request.POST.get('password')
        reenter_password = request.POST.get('reenterPassword')

        # Validate that passwords match
        if password != reenter_password:
            return render(request, 'restaurant/login.html', {'error': 'Passwords do not match'})

        try:
            # Verify the email and password in the Restaurant model
            restaurant_user = Restaurant.objects.get(emailId=email, password=password)
            request.session['user_id'] = str(restaurant_user.id)  # Convert UUID to string for session storage
            return redirect('restaurant:restaurant_home', restaurant_id=restaurant_user.id)
        except Restaurant.DoesNotExist:
            return render(request, 'restaurant/login.html', {'error': 'Invalid credentials'})

    return render(request, 'restaurant/login.html')


def profile(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'restaurant/profile.html', {'restaurant': restaurant})

def profile_edit(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.street = request.POST.get('street')
        restaurant.city = request.POST.get('city')
        restaurant.pincode = request.POST.get('pincode')
        restaurant.description = request.POST.get('description')
        restaurant.save()

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('restaurant:profile', restaurant_id=restaurant_id)

    return render(request, 'restaurant/profile_edit.html', {'restaurant': restaurant})

def restaurant_home(request, restaurant_id):
    user_id = request.session.get('user_id')
    if not user_id or user_id != str(restaurant_id): 
        return redirect('restaurant:login')
    
    restaurant_user = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'restaurant/home.html', {'restaurant': restaurant_user, 'restaurant_id': restaurant_id})

def about(request, restaurant_id):
    user_id = request.session.get('user_id')
    if not user_id or user_id != str(restaurant_id):
        return redirect('restaurant:login')
    
    restaurant_user = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'restaurant/about.html', {'restaurant': restaurant_user, 'restaurant_id': restaurant_id})

def orders(request, restaurant_id):
    user_id = request.session.get('user_id')
    if not user_id or user_id != str(restaurant_id):
        return redirect('restaurant:login')
    
    restaurant_user = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'restaurant/orders.html', {'restaurant': restaurant_user, 'restaurant_id': restaurant_id})

def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    user_id = request.session.get('user_id')
    
    if not user_id or user_id != str(restaurant_id):
        return redirect('restaurant:login')
    
    menu_items = restaurant.menu_items.all()
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.restaurant = restaurant
            new_item.save()
            return redirect('restaurant:restaurant_menu', restaurant_id=restaurant.id)
    else:
        form = MenuItemForm()

    return render(request, 'restaurant/restaurant_menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'form': form,
    })
    

def edit_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    restaurant = item.restaurant 

    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('restaurant:restaurant_menu', restaurant_id=restaurant.id)
    else:
        form = MenuItemForm(instance=item)

    return render(request, 'restaurant/edit_item.html', {'form': form, 'item': item, 'restaurant': restaurant})

def delete_item(request, item_id):
    if request.method == 'POST': 
        item = get_object_or_404(MenuItem, id=item_id) 
        restaurant_id = item.restaurant.id 
        item.delete() 
        return redirect('restaurant:restaurant_menu', restaurant_id=restaurant_id)  
    else:
        raise Http404("This action can only be performed via POST request.")
    
import json
def orders(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    orders = Order.objects.filter(restaurant=restaurant).order_by('-ordered_at')  

    for order in orders:
        try:
            order.ordered_items_json = json.dumps(order.ordered_items, indent=4)
        except Exception as e:
            order.ordered_items_json = f"Error: {e}"

    return render(request, 'restaurant/orders.html', {'orders': orders, 'restaurant': restaurant})

def customer_profile(request, restaurant_id, customer_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, 'restaurant/customer_profile.html', {'customer': customer, 'restaurant': restaurant})

def mark_order_done(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if str(order.restaurant.id) == request.session.get('user_id'):
        order.status = 'Cooking Done'
        order.save()

    return redirect('restaurant:orders', restaurant_id=order.restaurant.id)
