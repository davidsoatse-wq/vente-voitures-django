from django.urls import path
from django.contrib.auth import views as auth_views # Ajoute cet import
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('voiture/<int:pk>/', views.car_detail, name='car_detail'),
    # Remplace ta ligne login par celle-ci :
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    # Ajoute aussi la déconnexion pour que le bouton fonctionne :
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]