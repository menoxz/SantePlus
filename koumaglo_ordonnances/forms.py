from django import forms
from .models import Ordonnance, OrdonnanceDetail
from koumaglo_parametres.models import Medicament
import uuid
from django.forms import inlineformset_factory

class OrdonnanceForm(forms.ModelForm):
    code_ordonnance = forms.CharField(
        max_length=50,
        required=False,
        label='Code',
        help_text="Laissez vide pour générer automatiquement"
    )
    
    date_ordonnance = forms.DateTimeField(
        label='Date de l\'ordonnance',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    class Meta:
        model = Ordonnance
        fields = ['code_ordonnance', 'date_ordonnance']
    
    def clean_code_ordonnance(self):
        code = self.cleaned_data.get('code_ordonnance')
        if not code:
            code = f"ORD{uuid.uuid4().hex[:8].upper()}"
        return code

class OrdonnanceDetailForm(forms.ModelForm):
    code_ordonnance_detail = forms.CharField(
        max_length=50,
        required=False,
        label='Code',
        help_text="Laissez vide pour générer automatiquement"
    )
    
    medicament = forms.ModelChoiceField(
        queryset=Medicament.objects.all(),
        label='Médicament',
        widget=forms.Select(attrs={'class': 'form-control select2-field'})
    )
    
    posologie_medicament = forms.CharField(
        label='Posologie',
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
    )
    
    class Meta:
        model = OrdonnanceDetail
        fields = ['code_ordonnance_detail', 'medicament', 'posologie_medicament']
    
    def clean_code_ordonnance_detail(self):
        code = self.cleaned_data.get('code_ordonnance_detail')
        if not code:
            code = f"DET{uuid.uuid4().hex[:8].upper()}"
        return code

# Création d'un formset pour gérer plusieurs détails d'ordonnance en même temps
OrdonnanceDetailFormSet = inlineformset_factory(
    Ordonnance, 
    OrdonnanceDetail,
    form=OrdonnanceDetailForm,
    extra=1,  # Nombre de formulaires vides à afficher
    can_delete=True  # Permettre la suppression des détails existants
) 