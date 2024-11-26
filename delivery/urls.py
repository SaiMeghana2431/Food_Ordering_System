from django.urls import path
from . import views
from .views import delivery_home


app_name = 'delivery'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.delivery_home, name='delivery_home'),
    path('about/', views.about, name='about'),
    path('to_be_delivered/', views.to_be_delivered, name='to_be_delivered'),
    path('delivered/', views.delivered, name='delivered'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('mark_order_delivered/<int:order_id>/', views.mark_order_delivered, name='mark_order_delivered'),
]