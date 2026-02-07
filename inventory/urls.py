from django.urls import path
from django.contrib.auth import views as auth_views # Ajoute cet import
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('voiture/<int:pk>/', views.car_detail, name='car_detail'),

    # On utilise TES vues personnalisées pour garder le contrôle
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]