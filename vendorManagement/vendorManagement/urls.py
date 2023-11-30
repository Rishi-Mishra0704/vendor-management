from django.contrib import admin
from django.urls import path, include, re_path
from . import views


api_patterns = [

    path('', include('vendorApi.urls')),
    path('', include('purchaseApi.urls')),
    path('', include('historyApi.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
    path('login/', views.login),    
    path('signup/', views.signup),
]   
