from django import forms
from .models import Utilisateur

class UtilisateurProfilForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Nom d\'utilisateur',
            'email': 'Adresse email',
            'first_name': 'Prénom',
            'last_name': 'Nom',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input rounded-md border-gray-300 shadow-sm w-full py-2 px-3'}),
            'email': forms.EmailInput(attrs={'class': 'form-input rounded-md border-gray-300 shadow-sm w-full py-2 px-3'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input rounded-md border-gray-300 shadow-sm w-full py-2 px-3'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input rounded-md border-gray-300 shadow-sm w-full py-2 px-3'}),
        } 