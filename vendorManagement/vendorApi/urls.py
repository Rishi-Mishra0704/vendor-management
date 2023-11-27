from django.urls import path
from . import views

urlpatterns = [
    path('vendors/',views.vendors,name='vendors'),
]
