from django.db import models

# Create your models here.
from django.db import models

class Car(models.Model):
    brand = models.CharField(max_length=100, verbose_name="Marque")
    model = models.CharField(max_length=100, verbose_name="Modèle")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    year = models.IntegerField(verbose_name="Année")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='cars/', blank=True, null=True, verbose_name="Photo")
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"