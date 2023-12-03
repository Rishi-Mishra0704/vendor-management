# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('historical_performance/', views.index, name='index'),
]
