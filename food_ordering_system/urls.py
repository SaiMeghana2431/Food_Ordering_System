from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # Root URL points to accounts' select_role view
    path('customer/', include('customer.urls')),  # Customer routes
    path('delivery/', include('delivery.urls')),  # Delivery routes
    path('restaurant/', include('restaurant.urls')),  # Restaurant routes
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)