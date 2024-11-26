from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.select_role, name='select_role'), 
    path('redirect_login/', views.redirect_login, name='redirect_login'),
    path('logout/', views.logout, name='logout'),
]
