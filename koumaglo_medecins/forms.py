from django import forms
from .models import Medecin, Specialite, AffecterSpecialite
from koumaglo_patients.models import Personne
import uuid

class SpecialiteForm(forms.ModelForm):
    class Meta:
        model = Specialite
        fields = ['code', 'libelle']
        labels = {
            'code': 'Code',
            'libelle': 'Libellé',
        }
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MedecinFormComplet(forms.Form):
    # Champs pour Personne
    code = forms.CharField(max_length=50, label='Code', required=False,
                         help_text="Laissez vide pour générer automatiquement")
    nom = forms.CharField(max_length=100, label='Nom')
    prenom = forms.CharField(max_length=100, label='Prénom')
    date_naissance = forms.DateField(label='Date de Naissance',
                                   widget=forms.DateInput(attrs={'type': 'date'}))
    civilite = forms.ChoiceField(choices=[('M', 'Monsieur'), ('Mme', 'Madame'), ('Mlle', 'Mademoiselle')],
                               label='Civilité',
                               widget=forms.Select(attrs={'class': 'form-control select2-field'}))
    
    # Champs pour Médecin
    titre_medecin = forms.CharField(max_length=50, label='Titre')
    specialites = forms.ModelMultipleChoiceField(
        queryset=Specialite.objects.all(),
        label='Spécialités',
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2-field', 'multiple': 'multiple'}),
        required=False
    )
    
    def save(self):
        # Générer un code si nécessaire
        if not self.cleaned_data['code']:
            self.cleaned_data['code'] = f"MED{uuid.uuid4().hex[:8].upper()}"
        
        # Récupérer ou créer la personne
        personne, created = Personne.objects.update_or_create(
            code=self.cleaned_data['code'],
            defaults={
                'nom': self.cleaned_data['nom'],
                'prenom': self.cleaned_data['prenom'],
                'date_naissance': self.cleaned_data['date_naissance'],
                'civilite': self.cleaned_data['civilite']
            }
        )
        
        # Récupérer ou créer le médecin
        medecin, created = Medecin.objects.update_or_create(
            personne=personne,
            defaults={
                'titre_medecin': self.cleaned_data['titre_medecin']
            }
        )
        
        # Gérer les spécialités
        # Supprimer les anciennes affectations
        AffecterSpecialite.objects.filter(medecin=medecin).delete()
        
        # S'assurer que specialites est présent (même si vide)
        specialites_selectionnees = self.cleaned_data.get('specialites', [])
        
        # Journalisation pour débogage
        print(f"Spécialités sélectionnées : {specialites_selectionnees}")
        
        # Créer de nouvelles affectations pour chaque spécialité sélectionnée
        from datetime import date
        for specialite in specialites_selectionnees:
            AffecterSpecialite.objects.create(
                medecin=medecin,
                specialite=specialite,
                date_affectation=date.today(),
                actif=True
            )
        
        return medecin