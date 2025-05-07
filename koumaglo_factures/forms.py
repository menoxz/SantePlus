from django import forms
from .models import Facture, FactureDetail, Paiement
from koumaglo_consultations.models import Consultation
from koumaglo_parametres.models import Acte
from koumaglo_patients.models import Patient
import uuid
from django.forms import inlineformset_factory

class PatientSelectionForm(forms.Form):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        label='Sélectionner un patient',
        widget=forms.Select(attrs={'class': 'form-control select2-field'})
    )

class ConsultationSelectionForm(forms.Form):
    consultation = forms.ModelChoiceField(
        queryset=Consultation.objects.filter(factures__isnull=True),
        label='Sélectionner une consultation',
        widget=forms.Select(attrs={'class': 'form-control select2-field'}),
        help_text="Seules les consultations non facturées sont affichées"
    )
    
    def __init__(self, *args, **kwargs):
        patient_id = kwargs.pop('patient_id', None)
        super(ConsultationSelectionForm, self).__init__(*args, **kwargs)
        
        if patient_id:
            self.fields['consultation'].queryset = Consultation.objects.filter(
                patient_id=patient_id,
                factures__isnull=True
            )

class FactureForm(forms.ModelForm):
    code_facture = forms.CharField(
        max_length=50,
        required=False,
        label='Code',
        help_text="Laissez vide pour générer automatiquement"
    )
    
    type_facture = forms.ChoiceField(
        choices=[
            ('consultation', 'Consultation'),
            ('actes', 'Actes Médicaux'),
            ('medicaments', 'Médicaments'),
            ('autre', 'Autre')
        ],
        label='Type de facture',
        widget=forms.Select(attrs={'class': 'form-control select2-field'})
    )
    
    class Meta:
        model = Facture
        fields = ['code_facture', 'type_facture']
    
    def clean_code_facture(self):
        code = self.cleaned_data.get('code_facture')
        if not code:
            code = f"FACT{uuid.uuid4().hex[:8].upper()}"
        return code

class FactureDetailForm(forms.ModelForm):
    acte = forms.ModelChoiceField(
        queryset=Acte.objects.all(),
        label='Acte',
        widget=forms.Select(attrs={'class': 'form-control select2-field'})
    )
    
    montant_facture_detail = forms.DecimalField(
        label='Montant',
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    
    class Meta:
        model = FactureDetail
        fields = ['acte', 'montant_facture_detail']

class PaiementForm(forms.ModelForm):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Montant du paiement',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    paymentDate = forms.DateTimeField(
        label='Date du paiement',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    
    class Meta:
        model = Paiement
        fields = ['amount', 'paymentDate']
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        facture = self.instance.facture if hasattr(self.instance, 'facture') else None
        
        if facture:
            total_paye = sum(p.amount for p in facture.paiements.all() if p != self.instance)
            reste_a_payer = facture.montant_facture - total_paye
            
            if amount > reste_a_payer:
                raise forms.ValidationError(f"Le montant du paiement ne peut pas dépasser le reste à payer ({reste_a_payer} XOF)")
        
        return amount

# Création d'un formset pour gérer plusieurs détails de facture en même temps
FactureDetailFormSet = inlineformset_factory(
    Facture, 
    FactureDetail,
    form=FactureDetailForm,
    extra=1,
    can_delete=True
) 