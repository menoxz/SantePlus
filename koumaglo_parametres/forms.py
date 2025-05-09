from django import forms
from .models import Medicament, TypeActe, Acte
from koumaglo_medecins.models import Specialite, AffecterSpecialite
from koumaglo_consultations.models import Consultation
import uuid
from django.db import models

class MedicamentForm(forms.ModelForm):
    class Meta:
        model = Medicament
        fields = ['libelle_medicament', 'description']
        widgets = {
            'libelle_medicament': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }
        labels = {
            'libelle_medicament': 'Nom du médicament',
            'description': 'Description',
        }

class TypeActeForm(forms.ModelForm):
    specialites = forms.ModelMultipleChoiceField(
        queryset=Specialite.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select select2-field'}),
        required=False,
        label='Spécialités associées'
    )
    
    class Meta:
        model = TypeActe
        fields = ['libelle', 'description', 'specialites']
        widgets = {
            'libelle': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }
        labels = {
            'libelle': 'Libellé de l\'acte',
            'description': 'Description',
        }

class ActeForm(forms.ModelForm):
    class Meta:
        model = Acte
        fields = ['libelle_acte', 'montant_acte', 'type_acte', 'specialite', 'consultation']
        widgets = {
            'libelle_acte': forms.TextInput(attrs={'class': 'form-input'}),
            'montant_acte': forms.NumberInput(attrs={'class': 'form-input'}),
            'type_acte': forms.Select(attrs={'class': 'form-select select2-field'}),
            'specialite': forms.Select(attrs={'class': 'form-select select2-field'}),
            'consultation': forms.Select(attrs={'class': 'form-select select2-field'}),
        }
        labels = {
            'libelle_acte': 'Libellé de l\'acte',
            'montant_acte': 'Montant',
            'type_acte': 'Type d\'acte',
            'specialite': 'Spécialité',
            'consultation': 'Consultation'
        }
    
    def __init__(self, *args, **kwargs):
        consultation_id = kwargs.pop('consultation_id', None)
        super().__init__(*args, **kwargs)
        
        if consultation_id:
            self.fields['consultation'].initial = consultation_id
            self.fields['consultation'].widget = forms.HiddenInput()
            
            # Filtrer les actes en fonction de la spécialité du médecin de la consultation
            consultation = Consultation.objects.get(pk=consultation_id)
            medecin = consultation.medecin
            
            # Récupérer les spécialités actives du médecin
            specialites_medecin = [affectation.specialite for affectation in 
                                  AffecterSpecialite.objects.filter(medecin=medecin, actif=True)]
            
            # Sélectionner la première spécialité du médecin comme valeur par défaut
            if specialites_medecin:
                self.fields['specialite'].initial = specialites_medecin[0]
            
            # Filtrer les spécialités pour n'afficher que celles du médecin
            specialites_ids = [specialite.id for specialite in specialites_medecin]
            self.fields['specialite'].queryset = Specialite.objects.filter(id__in=specialites_ids)
            
            # Si aucune spécialité n'est disponible pour ce médecin, ajouter un message d'aide
            if not specialites_ids:
                self.fields['specialite'].help_text = "Ce médecin n'a aucune spécialité assignée."
        else:
            # Afficher seulement les consultations non facturées
            consultations_non_facturees = Consultation.objects.filter(factures__isnull=True)
            self.fields['consultation'].queryset = consultations_non_facturees
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.code_acte:
            instance.code_acte = f"ACT{uuid.uuid4().hex[:8].upper()}"
            
        # Assurons-nous que la consultation est correctement associée
        consultation_id = self.fields['consultation'].initial
        if consultation_id and not instance.consultation_id:
            from koumaglo_consultations.models import Consultation
            instance.consultation = Consultation.objects.get(pk=consultation_id)
            
        if commit:
            instance.save()
        return instance 

class ActeConsultationForm(forms.Form):
    acte = forms.ModelChoiceField(
        queryset=Acte.objects.filter(consultation__isnull=True),
        widget=forms.Select(attrs={'class': 'form-select select2-field'}),
        label='Sélectionner un acte',
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        consultation_id = kwargs.pop('consultation_id', None)
        super().__init__(*args, **kwargs)
        
        if consultation_id:
            # Récupérer la consultation et le médecin
            from koumaglo_consultations.models import Consultation
            consultation = Consultation.objects.get(pk=consultation_id)
            medecin = consultation.medecin
            
            # Récupérer les spécialités actives du médecin
            specialites_medecin = [affectation.specialite for affectation in 
                                  AffecterSpecialite.objects.filter(medecin=medecin, actif=True)]
            
            # Filtrer les actes qui correspondent aux spécialités du médecin
            specialites_ids = [specialite.id for specialite in specialites_medecin]
            
            # N'afficher que les actes qui sont disponibles (non liés à une consultation)
            actes_disponibles = Acte.objects.filter(consultation__isnull=True)
            
            # Si des spécialités sont trouvées, filtrer par spécialité
            if specialites_ids:
                # Inclure aussi les actes sans spécialité (null) pour compatibilité avec les données existantes
                actes_disponibles = actes_disponibles.filter(
                    models.Q(specialite__id__in=specialites_ids) | 
                    models.Q(specialite__isnull=True)
                )
            
            self.fields['acte'].queryset = actes_disponibles
            
            # Ajouter un message d'aide si aucun acte n'est disponible
            if not actes_disponibles.exists():
                self.fields['acte'].help_text = "Aucun acte disponible pour les spécialités de ce médecin. Veuillez créer un nouvel acte."
                self.fields['acte'].widget.attrs['disabled'] = 'disabled' 