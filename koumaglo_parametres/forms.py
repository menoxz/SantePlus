from django import forms
from .models import Medicament, TypeActe, Acte
from koumaglo_medecins.models import Specialite, AffecterSpecialite
from koumaglo_consultations.models import Consultation
import uuid

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
        fields = ['libelle_acte', 'montant_acte', 'type_acte', 'consultation']
        widgets = {
            'libelle_acte': forms.TextInput(attrs={'class': 'form-input'}),
            'montant_acte': forms.NumberInput(attrs={'class': 'form-input'}),
            'type_acte': forms.Select(attrs={'class': 'form-select select2-field'}),
            'consultation': forms.Select(attrs={'class': 'form-select select2-field'}),
        }
        labels = {
            'libelle_acte': 'Libellé de l\'acte',
            'montant_acte': 'Montant',
            'type_acte': 'Type d\'acte',
            'consultation': 'Consultation'
        }
    
    def __init__(self, *args, **kwargs):
        consultation_id = kwargs.pop('consultation_id', None)
        super().__init__(*args, **kwargs)
        if consultation_id:
            self.fields['consultation'].initial = consultation_id
            self.fields['consultation'].widget = forms.HiddenInput()
            
            # Filtrer les types d'actes en fonction de la spécialité du médecin de la consultation
            consultation = Consultation.objects.get(pk=consultation_id)
            medecin = consultation.medecin
            
            # Récupérer les spécialités actives du médecin
            specialites_medecin = [affectation.specialite for affectation in 
                                  AffecterSpecialite.objects.filter(medecin=medecin, actif=True)]
            
            # Filtrer les types d'actes qui sont liés à ces spécialités
            types_actes_ids = []
            for specialite in specialites_medecin:
                types_actes_ids.extend(TypeActe.objects.filter(specialites=specialite).values_list('id', flat=True))
            
            # Éliminer les doublons
            types_actes_ids = list(set(types_actes_ids))
            
            # Mettre à jour le queryset pour n'afficher que les types d'actes liés aux spécialités du médecin
            self.fields['type_acte'].queryset = TypeActe.objects.filter(id__in=types_actes_ids)
            
            # Si aucun type d'acte n'est disponible pour ce médecin, ajouter un message d'aide
            if not types_actes_ids:
                self.fields['type_acte'].help_text = "Aucun type d'acte n'est associé aux spécialités de ce médecin."
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