from django.shortcuts import render , get_object_or_404 #django affiche 404 au lieu de planter
from .models import Car

def home(request):
   #(ancien d'alex) cars = Car.objects.all() # On récupère toutes les voitures
    cars = Car.objects.filter(status='Disponible').order_by('-created_at')
   # On filtre pour vendre uniquement les voitures 'Disponibles'
   # Le '-' devant created_at permet de trier de la plus récente à la plus ancienne
    return render(request, 'inventory/home.html', {'cars': cars})

def car_detail(request, pk):
    #  fiche détaillée d'UNE SEULE voiture
    # pk (Primary Key) est l'identifiant unique de la voiture
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'inventory/car_detail.html', {'car': car})
#Attribué automatiquement


def login_view(request):
    return render(request, 'inventory/login.html')