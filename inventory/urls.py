from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('voiture/<int:pk>/', views.car_detail, name='car_detail'),
    path('login/', views.login_view, name='login'),
]
