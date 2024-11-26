from django.shortcuts import get_object_or_404, render, redirect
from .forms import DeliverySignupForm
from django.contrib.auth import authenticate, login
from .models import Delivery
from customer.models import Order
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.timezone import now

def signup(request):
    if request.method == 'POST':
        form = DeliverySignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('delivery:login')
    else:
        form = DeliverySignupForm()
    return render(request, 'delivery/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('emailId')
        password = request.POST.get('password')
        
        try:
            delivery_user = Delivery.objects.get(emailId=email, password=password) 
            request.session['user_id'] = delivery_user.id  
            return redirect('delivery:delivery_home') 
        except Delivery.DoesNotExist:
            return render(request, 'delivery/login.html', {'error': 'Invalid credentials'})

    return render(request, 'delivery/login.html')

def delivery_home(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('delivery:login') 
    
    delivery_user = Delivery.objects.get(id=user_id)
    return render(request, 'delivery/home.html', {'user': delivery_user})

def about(request):
    return render(request, 'delivery/about.html')

def profile_view(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('delivery:login') 
    try:
        delivery = Delivery.objects.get(id=user_id)
    except Delivery.DoesNotExist:
        return redirect('delivery:login')
    
    return render(request, 'delivery/profile.html', {'user': delivery})

def profile_edit(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('delivery:login')  

    try:
        delivery = Delivery.objects.get(id=user_id)
    except Delivery.DoesNotExist:
        return redirect('delivery:login')

    if request.method == 'POST':
        delivery.name = request.POST['name']
        delivery.city = request.POST['city']
        delivery.save()

        return redirect('delivery:profile')  

    return render(request, 'delivery/profile_edit.html', {'user': delivery})

def to_be_delivered(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('delivery:login') 

    pending_orders = Order.objects.filter(status__in=["Cooking Done", "Pending"]).select_related('customer', 'restaurant')
    return render(request, 'delivery/to_be_delivered.html', {'orders': pending_orders})

def delivered(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('delivery:login')

    delivered_orders = Order.objects.filter(status="Delivered").select_related('customer', 'restaurant')
    return render(request, 'delivery/delivered.html', {'orders': delivered_orders})

def mark_order_delivered(request, order_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('delivery:login') 

    order = get_object_or_404(Order, id=order_id)

    if order.status == "Cooking Done":
        order.status = "Delivered"
        order.delivery_datetime = now()
        order.save()

        items_details = "\n".join([f"{item['item_name']} - Quantity: {item['quantity']}" for item in order.ordered_items])
        print(f"Ordered items: {items_details}")

        try:
            send_mail(
                'Order Delivered',
                f"Dear {order.customer.name},\n\nYour order has been successfully delivered to you.\n\nItems:\n{items_details}\n\nThank you for using our service!",
                'meghananaidu0331@gmail.com', 
                [order.customer.emailId],
                fail_silently=False,
            )
            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending email: {e}")

        messages.success(request, f"Order {order.id} marked as delivered.")

    return redirect('delivery:to_be_delivered')