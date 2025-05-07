from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string, get_template
from django.utils import timezone
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from io import BytesIO
import uuid

from .models import Facture, FactureDetail, Paiement
from .forms import FactureDetailFormSet, PatientSelectionForm, ConsultationSelectionForm, FactureForm, PaiementForm
from koumaglo_consultations.models import Consultation
from koumaglo_patients.models import Patient
from koumaglo_parametres.models import Acte

@login_required
def facture_list(request):
    factures = Facture.objects.all().order_by('-date_enreg_facture')
    return render(request, 'koumaglo_factures/facture_list.html', {'factures': factures})

@login_required
def facture_detail(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    paiements = facture.paiements.all().order_by('-paymentDate')
    
    # Calculer le montant restant à payer
    montant_paye = paiements.aggregate(total=Sum('amount'))['total'] or 0
    montant_restant = facture.montant_facture - montant_paye
    
    # Formulaire de paiement
    if request.method == 'POST' and 'paiement_submit' in request.POST:
        paiement_form = PaiementForm(request.POST)
        if paiement_form.is_valid():
            paiement = paiement_form.save(commit=False)
            paiement.facture = facture
            paiement.save()
            
            # Mise à jour du montant payé de la facture
            facture.montant_paye_facture = Paiement.objects.filter(facture=facture).aggregate(total=Sum('amount'))['total'] or 0
            
            # Si tout est payé, mettre à jour la date de paiement
            if facture.montant_paye_facture >= facture.montant_facture:
                facture.date_paiement_facture = timezone.now()
            
            facture.save()
            
            messages.success(request, "Le paiement a été enregistré avec succès.")
            return redirect('koumaglo_factures:facture_detail', pk=facture.pk)
    else:
        paiement_form = PaiementForm(initial={'paymentDate': timezone.now()})
    
    context = {
        'facture': facture,
        'paiements': paiements,
        'montant_paye': montant_paye,
        'montant_restant': montant_restant,
        'paiement_form': paiement_form,
    }
    
    return render(request, 'koumaglo_factures/facture_detail.html', context)

@login_required
def facture_add(request, consultation_id=None):
    consultation = None
    if consultation_id:
        consultation = get_object_or_404(Consultation, pk=consultation_id)
    
    if request.method == 'POST':
        form = FactureForm(request.POST)
        
        if form.is_valid():
            with transaction.atomic():
                facture = form.save(commit=False)
                # Si la consultation est fournie directement, l'utiliser
                if consultation and not facture.consultation:
                    facture.consultation = consultation
                
                # Définir l'utilisateur courant comme créateur de la facture
                facture.utilisateur = request.user
                # Médecin de la consultation comme référent de la facture
                facture.medecin = facture.consultation.medecin
                
                # Initialiser le montant à 0, il sera calculé après
                facture.montant_facture = 0
                facture.save()
                
                # Traitement du formset pour les détails de la facture
                formset = FactureDetailFormSet(request.POST, instance=facture)
                if formset.is_valid():
                    formset.save()
                    
                    # Mettre à jour le montant total de la facture
                    total = FactureDetail.objects.filter(facture=facture).aggregate(total=Sum('montant_facture_detail'))['total'] or 0
                    facture.montant_facture = total
                    facture.save()
                    
                    messages.success(request, "La facture a été créée avec succès.")
                    return redirect('koumaglo_factures:facture_detail', pk=facture.pk)
                else:
                    # Si le formset n'est pas valide, supprimer la facture
                    facture.delete()
                    messages.error(request, "Erreur dans les détails de la facture.")
    else:
        initial_data = {}
        if consultation:
            initial_data = {'consultation': consultation}
        
        form = FactureForm(initial=initial_data)
        formset = FactureDetailFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'consultation': consultation,
        'mode': 'ajouter'
    }
    return render(request, 'koumaglo_factures/facture_form.html', context)

@login_required
def facture_edit(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    
    # Vérifier si la facture est déjà payée
    if facture.date_paiement_facture:
        messages.error(request, "Impossible de modifier une facture déjà payée.")
        return redirect('koumaglo_factures:facture_detail', pk=facture.pk)
    
    if request.method == 'POST':
        form = FactureForm(request.POST, instance=facture)
        
        if form.is_valid():
            with transaction.atomic():
                facture = form.save()
                
                # Traitement du formset pour les détails de la facture
                formset = FactureDetailFormSet(request.POST, instance=facture)
                if formset.is_valid():
                    formset.save()
                    
                    # Mettre à jour le montant total de la facture
                    total = FactureDetail.objects.filter(facture=facture).aggregate(total=Sum('montant_facture_detail'))['total'] or 0
                    facture.montant_facture = total
                    facture.save()
                    
                    messages.success(request, "La facture a été modifiée avec succès.")
                    return redirect('koumaglo_factures:facture_detail', pk=facture.pk)
                else:
                    messages.error(request, "Erreur dans les détails de la facture.")
    else:
        form = FactureForm(instance=facture)
        formset = FactureDetailFormSet(instance=facture)
    
    context = {
        'form': form,
        'formset': formset,
        'facture': facture,
        'mode': 'modifier'
    }
    return render(request, 'koumaglo_factures/facture_form.html', context)

@login_required
def facture_delete(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    
    # Vérifier si la facture est déjà payée
    if facture.date_paiement_facture:
        messages.error(request, "Impossible de supprimer une facture déjà payée.")
        return redirect('koumaglo_factures:facture_detail', pk=facture.pk)
    
    if request.method == 'POST':
        consultation = facture.consultation
        facture.delete()
        messages.success(request, "La facture a été supprimée avec succès.")
        return redirect('koumaglo_consultations:consultation_detail', pk=consultation.pk)
    
    return render(request, 'koumaglo_factures/facture_confirm_delete.html', {'facture': facture})

@login_required
def select_patient_for_facture(request):
    if request.method == 'POST':
        form = PatientSelectionForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            return redirect('koumaglo_factures:select_consultation', patient_id=patient.pk)
    else:
        form = PatientSelectionForm()
    
    return render(request, 'koumaglo_factures/select_patient.html', {'form': form})

@login_required
def select_consultation(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    
    if request.method == 'POST':
        form = ConsultationSelectionForm(request.POST, patient_id=patient_id)
        if form.is_valid():
            consultation = form.cleaned_data['consultation']
            return redirect('koumaglo_factures:facture_preview', consultation_id=consultation.pk)
    else:
        form = ConsultationSelectionForm(patient_id=patient_id)
    
    if form.fields['consultation'].queryset.count() == 0:
        messages.warning(request, f"Le patient {patient} n'a pas de consultations non facturées.")
    
    return render(request, 'koumaglo_factures/select_consultation.html', {
        'form': form,
        'patient': patient
    })

@login_required
def facture_preview(request, consultation_id):
    consultation = get_object_or_404(Consultation, pk=consultation_id)
    actes = consultation.actes.all()
    
    # Calculer le montant total
    montant_total = actes.aggregate(total=Sum('montant_acte'))['total'] or 0
    
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Créer la facture
                facture = form.save(commit=False)
                facture.consultation = consultation
                facture.montant_facture = montant_total
                facture.utilisateur = request.user
                facture.medecin = consultation.medecin
                facture.save()
                
                # Créer les détails de la facture à partir des actes
                for acte in actes:
                    FactureDetail.objects.create(
                        facture=facture,
                        acte=acte,
                        code_detail_facture=f"DET{uuid.uuid4().hex[:8].upper()}",
                        montant_facture_detail=acte.montant_acte
                    )
                
                messages.success(request, "La facture a été créée avec succès.")
                return redirect('koumaglo_factures:facture_detail', pk=facture.pk)
    else:
        form = FactureForm()
    
    return render(request, 'koumaglo_factures/facture_preview.html', {
        'form': form,
        'consultation': consultation,
        'actes': actes,
        'montant_total': montant_total
    })

@login_required
def get_acte_montant(request, acte_id):
    """API pour récupérer le montant d'un acte en AJAX"""
    acte = get_object_or_404(Acte, pk=acte_id)
    return HttpResponse(str(acte.montant_acte))

@login_required
def facture_pdf(request, pk):
    """Génère un PDF pour une facture spécifique"""
    facture = get_object_or_404(Facture, pk=pk)
    paiements = facture.paiements.all().order_by('-paymentDate')
    
    # Calculer le montant payé et restant
    montant_paye = paiements.aggregate(total=Sum('amount'))['total'] or 0
    montant_restant = facture.montant_facture - montant_paye
    
    # Préparer le contexte
    context = {
        'facture': facture,
        'paiements': paiements,
        'montant_paye': montant_paye,
        'montant_restant': montant_restant,
    }
    
    # Rendre le template HTML
    template = get_template('koumaglo_factures/facture_pdf.html')
    html_string = template.render(context)
    
    # Configuration WeasyPrint
    font_config = FontConfiguration()
    html = HTML(string=html_string)
    
    # Générer le PDF
    result = BytesIO()
    html.write_pdf(target=result, font_config=font_config)
    
    # Créer la réponse HTTP avec le PDF
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{facture.code_facture}.pdf"'
    
    return response
