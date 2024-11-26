from django.urls import path
from . import views 
from .views import customer_home  

app_name = 'customer'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  
    path('home/', customer_home, name='customer_home'), 
    path('about/', views.about, name='about'),
    path('food_items/', views.food_items, name='food_items'),
    path('restaurant/<uuid:restaurant_id>/menu/', views.menu, name='menu'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('ordered-items/', views.ordered_items, name='ordered_items'),
    path('profile/', views.profile_view, name='profile'),  
    path('profile/edit/', views.profile_edit, name='edit_profile'),
]
