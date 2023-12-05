from django.contrib import admin
from django.urls import path, include
from . import views

api_patterns = [

    path('', include('vendorApi.urls')),
    path('', include('purchaseApi.urls')),
    path('', include('historyApi.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]
