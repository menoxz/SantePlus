from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from io import BytesIO
import datetime
from django.conf import settings
import os

from .models import Ordonnance, OrdonnanceDetail
from .forms import OrdonnanceForm, OrdonnanceDetailFormSet
from koumaglo_consultations.models import Consultation

@login_required
def ordonnance_list(request):
    ordonnances = Ordonnance.objects.all().order_by('-date_ordonnance')
    return render(request, 'koumaglo_ordonnances/ordonnance_list.html', {'ordonnances': ordonnances})

@login_required
def ordonnance_detail(request, pk):
    ordonnance = get_object_or_404(Ordonnance, pk=pk)
    return render(request, 'koumaglo_ordonnances/ordonnance_detail.html', {'ordonnance': ordonnance})

@login_required
def ordonnance_add(request, consultation_id=None):
    consultation = None
    if consultation_id:
        consultation = get_object_or_404(Consultation, pk=consultation_id)
    
    if request.method == 'POST':
        form = OrdonnanceForm(request.POST)
        formset = OrdonnanceDetailFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                ordonnance = form.save(commit=False)
                if consultation:
                    ordonnance.consultation = consultation
                ordonnance.save()
                
                # Associer le formset à l'ordonnance
                formset.instance = ordonnance
                formset.save()
                
                messages.success(request, "L'ordonnance a été créée avec succès.")
                if consultation:
                    return redirect('koumaglo_consultations:consultation_detail', pk=consultation.pk)
                return redirect('koumaglo_ordonnances:ordonnance_detail', pk=ordonnance.pk)
        else:
            # En cas d'erreur, afficher les messages d'erreur
            if not form.is_valid():
                messages.error(request, "Erreur dans le formulaire d'ordonnance.")
            if not formset.is_valid():
                messages.error(request, "Erreur dans les détails de l'ordonnance.")
    else:
        initial_data = {}
        if consultation:
            initial_data = {'consultation': consultation}
        form = OrdonnanceForm(initial=initial_data)
        formset = OrdonnanceDetailFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'consultation': consultation,
        'mode': 'ajouter'
    }
    return render(request, 'koumaglo_ordonnances/ordonnance_form.html', context)

@login_required
def ordonnance_edit(request, pk):
    ordonnance = get_object_or_404(Ordonnance, pk=pk)
    consultation = ordonnance.consultation
    
    if request.method == 'POST':
        form = OrdonnanceForm(request.POST, instance=ordonnance)
        formset = OrdonnanceDetailFormSet(request.POST, instance=ordonnance)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                ordonnance = form.save()
                formset.save()
                messages.success(request, "L'ordonnance a été modifiée avec succès.")
                return redirect('koumaglo_ordonnances:ordonnance_detail', pk=ordonnance.pk)
        else:
            if not form.is_valid():
                messages.error(request, "Erreur dans le formulaire d'ordonnance.")
            if not formset.is_valid():
                messages.error(request, "Erreur dans les détails de l'ordonnance.")
    else:
        form = OrdonnanceForm(instance=ordonnance)
        formset = OrdonnanceDetailFormSet(instance=ordonnance)
    
    context = {
        'form': form,
        'formset': formset,
        'ordonnance': ordonnance,
        'consultation': consultation,
        'mode': 'modifier'
    }
    return render(request, 'koumaglo_ordonnances/ordonnance_form.html', context)

@login_required
def ordonnance_delete(request, pk):
    ordonnance = get_object_or_404(Ordonnance, pk=pk)
    consultation = ordonnance.consultation
    
    if request.method == 'POST':
        ordonnance.delete()
        messages.success(request, "L'ordonnance a été supprimée avec succès.")
        return redirect('koumaglo_consultations:consultation_detail', pk=consultation.pk)
    
    return render(request, 'koumaglo_ordonnances/ordonnance_confirm_delete.html', {'ordonnance': ordonnance})

@login_required
def ordonnance_pdf(request, pk):
    ordonnance = get_object_or_404(Ordonnance, pk=pk)
    
    # Créer un objet HttpResponse avec le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ordonnance_{ordonnance.code_ordonnance}.pdf"'
    
    # Créer un fichier PDF
    buffer = BytesIO()
    
    # Créer le document PDF
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Définition des styles
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleH = styles["Heading1"]
    styleH2 = styles["Heading2"]
    
    # En-tête avec logo stylisé (sans utiliser d'image)
    p.setFillColorRGB(0.05, 0.58, 0.53)  # Couleur teal (similaire à #0D9488)
    p.setFont("Helvetica-Bold", 26)
    p.drawString(50, height - 60, "SantePlus")
    
    # Ligne de séparation teal
    p.setStrokeColorRGB(0.05, 0.58, 0.53)
    p.setLineWidth(2)
    p.line(50, height - 70, 150, height - 70)
    
    # Informations de la clinique
    p.setFillColorRGB(0, 0, 0)  # Retour à la couleur noire
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 100, "CLINIQUE SANTÉ PLUS")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 120, "Adresse: 123 Avenue de la Santé, Lomé, Togo")
    p.drawString(50, height - 140, "Téléphone: +228 12 34 56 78")
    p.drawString(50, height - 160, "Email: contact@santeplus.com")
    
    # Ligne séparatrice
    p.setLineWidth(1)
    p.setStrokeColorRGB(0, 0, 0)  # Ligne noire
    p.line(50, height - 180, width - 50, height - 180)
    
    # Titre
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width/2, height - 200, "ORDONNANCE MÉDICALE")
    
    # Informations de l'ordonnance
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 230, f"N° : {ordonnance.code_ordonnance}")
    p.drawString(50, height - 250, f"Date : {ordonnance.date_ordonnance.strftime('%d/%m/%Y')}")
    
    # Informations du patient
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 290, "PATIENT :")
    p.setFont("Helvetica", 12)
    p.drawString(150, height - 290, f"{ordonnance.consultation.patient.personne.civilite} {ordonnance.consultation.patient.personne.nom} {ordonnance.consultation.patient.personne.prenom}")
    
    # Informations du médecin
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 320, "MÉDECIN :")
    p.setFont("Helvetica", 12)
    p.drawString(150, height - 320, f"{ordonnance.consultation.medecin.titre_medecin} {ordonnance.consultation.medecin.personne.nom} {ordonnance.consultation.medecin.personne.prenom}")
    
    # Liste des médicaments
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 370, "PRESCRIPTION :")
    
    y = height - 400
    
    if ordonnance.details.all():
        for i, detail in enumerate(ordonnance.details.all(), 1):
            p.setFont("Helvetica-Bold", 12)
            p.drawString(60, y, f"{i}. {detail.medicament.libelle_medicament}")
            
            # Posologie - Wrap text to fit the page
            p.setFont("Helvetica", 11)
            posologie_lines = []
            for line in detail.posologie_medicament.split('\n'):
                posologie_lines.append(line)
            
            line_height = 20
            for line in posologie_lines:
                y -= line_height
                p.drawString(80, y, line)
            
            y -= 30  # Espace entre les médicaments
    else:
        p.setFont("Helvetica-Oblique", 12)
        p.drawString(60, y, "Aucun médicament prescrit.")
    
    # Pied de page et signature
    p.line(50, 120, width - 50, 120)
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 100, "Date et signature :")
    p.drawString(width - 200, 100, f"Lomé, le {datetime.datetime.now().strftime('%d/%m/%Y')}")
    
    # Signature du médecin
    p.line(width - 200, 60, width - 50, 60)
    p.setFont("Helvetica", 10)
    p.drawString(width - 200, 45, f"{ordonnance.consultation.medecin.titre_medecin} {ordonnance.consultation.medecin.personne.nom}")
    
    # Finalize the PDF
    p.showPage()
    p.save()
    
    # Récupérer le contenu du buffer et l'écrire dans la réponse
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response
