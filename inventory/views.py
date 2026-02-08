from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from datetime import datetime
from .models import Car
from .forms import InscriptionForm , AppointmentForm
# --- METTRE A JOUR L'Année ---
def home(request):
    return render(request, "inventory/home.html", {
        "year": datetime.now().year
    })
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

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'inventory/car_list.html', {'cars': cars})


@login_required
def appointment_create(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.car = car
            appointment.save()
            messages.success(request, "Votre demande de rendez-vous a été envoyée !")
            return redirect('car_detail', pk=car.id)
    else:
        form = AppointmentForm()

    return render(request, 'inventory/appointment_form.html', {'form': form, 'car': car})