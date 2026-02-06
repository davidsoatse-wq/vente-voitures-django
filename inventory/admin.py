from django.contrib import admin
from django.contrib import admin
from .models import Car
from django.utils.html import format_html

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price', 'kilometrage', 'status', 'created_at') #tableau de bord professionnel

    search_fields = ('brand', 'model', 'city') #C'est une barre de saisie de texte. Elle est utile quand tu ne sais pas exactement
    # ce que tu cherches ou quand il y a trop de possibilités à l'aide d'un mot clé.

    list_filter = ('brand', 'fuel', 'transmission', 'status', 'city') # menus cliquables,

    list_editable = ('status',) # valide  la publication de la voiture ,trier les données par groupes

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height:auto; border-radius:5px;" />', obj.image.url)
        return "Pas d'image"

    display_image.short_description = 'Aperçu'