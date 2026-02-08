from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from datetime import datetime
from .models import Car
from .forms import InscriptionForm , AppointmentForm
from django.db.models import Q

# --- METTRE A JOUR L'Année ---
def home(request):
    return render(request, "inventory/home.html", {
        "year": datetime.now().year
    })
# --- ACCUEIL ---
def home(request):
    # On récupère le texte de la barre de recherche
    query = request.GET.get('q')

    # ÉTAPE 1 : On commence par charger toutes les voitures (comportement par défaut)
    cars = Car.objects.filter(status='Disponible').order_by('-created_at')

    # ÉTAPE 2 : Si l'utilisateur a tapé quelque chose, on affine la liste
    if query:
        cars = cars.filter(
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(city__icontains=query)
        )

    # ÉTAPE 3 : On affiche les voitures (soit toutes, soit filtrées)
    return render(request, 'inventory/home.html', {
        'cars': cars,
        'year': datetime.now().year,
        'query': query
    })
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


@login_required
def vip_cars(request):
    # On définit ce qu'est une voiture VIP (ex: prix > 20 millions ou statut spécial)
    # Ici, on filtre les voitures dont le prix est supérieur à 20 000 000 FCFA
    cars_vip = Car.objects.filter(price__gte=20000000, status='Disponible').order_by('-price')

    return render(request, 'inventory/vip_cars.html', {
        'cars': cars_vip,
        'year': datetime.now().year
    })