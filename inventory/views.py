from django.shortcuts import render , get_object_or_404 #django affiche 404 au lieu de planter
from .models import Car

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Car
from .forms import InscriptionForm  # Le formulaire qu'on a créé ensemble

# --- ACCUEIL ---
def home(request):
    cars = Car.objects.filter(status='Disponible').order_by('-created_at')
    return render(request, 'inventory/home.html', {'cars': cars})

# --- DÉTAILS VOITURE ---
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'inventory/car_detail.html', {'car': car})

# --- INSCRIPTION (Username + Password) ---
def register_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès ! Connectez-vous.")
            return redirect('login')
    else:
        form = InscriptionForm()
    return render(request, 'inventory/register.html', {'form': form})

# --- CONNEXION ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = AuthenticationForm()
    return render(request, 'inventory/login.html', {'form': form})

# --- DÉCONNEXION ---
def logout_view(request):
    logout(request)
    return redirect('home')