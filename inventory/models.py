from django.db import models
from django.contrib.auth.models import User

class Car(models.Model): # Options pour les menus deroulants
    CARBURANT_CHOICES = [
        ('Essence', 'Essence'),
        ('Diesel', 'Diesel'),
        ('Hybride', 'Hybride'),
        ('Electrique', 'Électrique'),
    ]
    BOITE_CHOICES = [
        ('Manuelle', 'Manuelle'),
        ('Automatique', 'Automatique'),
    ]
    STATUT_CHOICES = [
        ('Disponible', 'Disponible'),
        ('Vendu', 'Vendu'),
        ('En attente', 'En attente de validation'),
    ]
    brand = models.CharField(max_length=100, verbose_name="Marque") #marques
    model = models.CharField(max_length=100, verbose_name="Modèle")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    year = models.IntegerField(verbose_name="Année") #annee de mise en circulation

    kilometrage = models.IntegerField(default=0, verbose_name="Kilométrage")  # Indique l'usure de la voiture.
    fuel = models.CharField(max_length=20, choices=CARBURANT_CHOICES, default='Essence', verbose_name="Carburant")  #carbuant
    transmission = models.CharField(max_length=20, choices=BOITE_CHOICES, default='Manuelle', verbose_name="Boîte de vitesse")  #auto ou manuelle
    city = models.CharField(max_length=100, default="Yaoundé", verbose_name="Ville")  #
    status = models.CharField(max_length=20, choices=STATUT_CHOICES, default='En attente', verbose_name="Statut")  #si l'admin l'a deja autorisé a vendre

    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='cars/', blank=True, null=True, verbose_name="Photo principale")  #
    created_at = models.DateTimeField(auto_now_add=True) # date creation

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) - {self.price} FCFA"


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email")
    date_rdv = models.DateTimeField(verbose_name="Date et Heure")
    message = models.TextField(blank=True, verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RDV de {self.user.username} pour {self.car.brand}"

