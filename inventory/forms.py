from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class InscriptionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username'] # On ne garde que le nom d'utilisateur, le mot de passe est géré par UserCreationForm