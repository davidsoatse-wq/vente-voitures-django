from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Appointment


# Ton formulaire d'inscription
class InscriptionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username'] # Le mot de passe est géré automatiquement par UserCreationForm

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['phone', 'email', 'date_rdv', 'message']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+237...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemple@mail.com'}),
            'date_rdv': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }