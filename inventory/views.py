from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from datetime import datetime
from .models import Car, Favorite  # <-- N'oublie pas d'ajouter Favorite ici
from .forms import InscriptionForm, AppointmentForm
from django.db.models import Q


# --- ACCUEIL ---
def home(request):
    query = request.GET.get('q')
    cars = Car.objects.filter(status='Disponible').order_by('-created_at')

    if query:
        cars = cars.filter(
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(city__icontains=query)
        )

    # On récupère les IDs des voitures aimées par l'utilisateur connecté
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('car_id', flat=True)

    return render(request, 'inventory/home.html', {
        'cars': cars,
        'year': datetime.now().year,
        'query': query,
        'user_favorites': user_favorites  # <-- On envoie ça au template
    })


# --- GESTION DES FAVORIS (Ajouter/Retirer) ---
@login_required
def toggle_favorite(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    # Si le favori existe, on le supprime, sinon on le crée
    favorite, created = Favorite.objects.get_or_create(user=request.user, car=car)

    if not created:
        favorite.delete()
        messages.info(request, f"{car.brand} retirée des favoris.")
    else:
        messages.success(request, f"{car.brand} ajoutée aux favoris !")

    # On redirige vers la page où l'utilisateur était
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# --- PAGE DES FAVORIS ---
@login_required
def favorite_list(request):
    # On récupère tous les objets favoris de l'utilisateur
    my_favorites = Favorite.objects.filter(user=request.user).select_related('car')
    return render(request, 'inventory/favorites.html', {
        'favorites': my_favorites,
        'year': datetime.now().year
    })


# --- DÉTAILS VOITURE ---
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'inventory/car_detail.html', {'car': car})


# --- INSCRIPTION ---
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


# --- RENDEZ-VOUS ---
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


# --- SECTION VIP ---
@login_required
def vip_cars(request):
    cars_vip = Car.objects.filter(price__gte=20000000, status='Disponible').order_by('-price')
    return render(request, 'inventory/vip_cars.html', {
        'cars': cars_vip,
        'year': datetime.now().year
    })