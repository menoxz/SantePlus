from django import forms
from .models import Consultation
from koumaglo_patients.models import Patient
from koumaglo_medecins.models import Medecin
import uuid

class ConsultationForm(forms.ModelForm):
    code_consultation = forms.CharField(
        max_length=50,
        required=False,
        label='Code',
        help_text="Laissez vide pour générer automatiquement"
    )
    
    date_consultation = forms.DateTimeField(
        label='Date de consultation',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    date_fin_validite_consultation = forms.DateTimeField(
        label='Date de fin de validité',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        label='Patient',
        widget=forms.Select(attrs={'class': 'form-control select2-field'}),
        required=True,
        empty_label=None
    )
    
    medecin = forms.ModelChoiceField(
        queryset=Medecin.objects.all(),
        label='Médecin',
        widget=forms.Select(attrs={'class': 'form-control select2-field'}),
        required=True,
        empty_label=None
    )
    
    class Meta:
        model = Consultation
        fields = ['code_consultation', 'date_consultation', 'date_fin_validite_consultation', 'patient', 'medecin']
    
    def clean_code_consultation(self):
        code = self.cleaned_data.get('code_consultation')
        if not code:
            code = f"CS{uuid.uuid4().hex[:8].upper()}"
        return code 