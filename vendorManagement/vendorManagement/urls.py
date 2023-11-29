from django.contrib import admin
from django.urls import path, include


api_patterns = [
    path('', include('vendorApi.urls')),
    path('', include('purchaseApi.urls')),
    path('', include('historyApi.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
]
