from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Car

def home(request):
    cars = Car.objects.all() # On récupère toutes les voitures
    return render(request, 'inventory/home.html', {'cars': cars})