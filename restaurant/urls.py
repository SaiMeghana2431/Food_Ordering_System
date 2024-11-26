# urls.py
from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('<uuid:restaurant_id>/profile/', views.profile, name='profile'),
    path('<uuid:restaurant_id>/profile/edit/', views.profile_edit, name='profile_edit'),
    path('<uuid:restaurant_id>/home/', views.restaurant_home, name='restaurant_home'),
    path('<uuid:restaurant_id>/about/', views.about, name='about'),
    path('<uuid:restaurant_id>/orders/', views.orders, name='orders'), 
    path('<uuid:restaurant_id>/customer/<int:customer_id>/profile/', views.customer_profile, name='customer_profile'),
    path('<uuid:restaurant_id>/menu/', views.restaurant_menu, name='restaurant_menu'),
    path('order/<int:order_id>/mark_done/', views.mark_order_done, name='mark_order_done'),
    path('menu/edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
]
