from django import forms
from .models import Personne, Patient
import uuid

class PersonneForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['code', 'nom', 'prenom', 'date_naissance', 'civilite']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'code': 'Code',
            'nom': 'Nom',
            'prenom': 'Prénom',
            'date_naissance': 'Date de Naissance',
            'civilite': 'Civilité',
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = []  # Aucun champ supplémentaire pour Patient, car il est lié à Personne

class PatientFormComplet(forms.Form):
    code = forms.CharField(max_length=50, label='Code', required=False, 
                         help_text='Laissez vide pour générer automatiquement')
    nom = forms.CharField(max_length=100, label='Nom')
    prenom = forms.CharField(max_length=100, label='Prénom')
    date_naissance = forms.DateField(label='Date de Naissance', 
                                   widget=forms.DateInput(attrs={'type': 'date'}))
    civilite = forms.ChoiceField(choices=[('M', 'Monsieur'), ('Mme', 'Madame'), ('Mlle', 'Mademoiselle')],
                              label='Civilité')
    
    def save(self):
        if not self.cleaned_data['code']:
            # Générer un code unique automatiquement
            self.cleaned_data['code'] = f"P{uuid.uuid4().hex[:8].upper()}"
            
        # Créer ou récupérer une personne
        personne, created = Personne.objects.get_or_create(
            code=self.cleaned_data['code'],
            defaults={
                'nom': self.cleaned_data['nom'],
                'prenom': self.cleaned_data['prenom'],
                'date_naissance': self.cleaned_data['date_naissance'],
                'civilite': self.cleaned_data['civilite']
            }
        )
        
        if not created:
            # Mettre à jour la personne si elle existe déjà
            personne.nom = self.cleaned_data['nom']
            personne.prenom = self.cleaned_data['prenom']
            personne.date_naissance = self.cleaned_data['date_naissance']
            personne.civilite = self.cleaned_data['civilite']
            personne.save()
        
        # Créer ou récupérer un patient lié à cette personne
        patient, created = Patient.objects.get_or_create(personne=personne)
        
        return patient 