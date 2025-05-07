from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Consultation
from .forms import ConsultationForm
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

@login_required
def consultation_list(request):
    consultations = Consultation.objects.all().order_by('-date_consultation')
    
    # Recherche par code
    code_query = request.GET.get('code', '')
    if code_query:
        consultations = consultations.filter(code_consultation__icontains=code_query)
    
    # Filtre par patient
    patient_query = request.GET.get('patient', '')
    if patient_query:
        consultations = consultations.filter(
            Q(patient__personne__nom__icontains=patient_query) | 
            Q(patient__personne__prenom__icontains=patient_query)
        )
    
    # Filtre par médecin
    medecin_query = request.GET.get('medecin', '')
    if medecin_query:
        consultations = consultations.filter(
            Q(medecin__personne__nom__icontains=medecin_query) | 
            Q(medecin__personne__prenom__icontains=medecin_query)
        )
    
    # Filtre par date (début)
    date_debut = request.GET.get('date_debut', '')
    if date_debut:
        try:
            date_debut = datetime.strptime(date_debut, '%Y-%m-%d')
            consultations = consultations.filter(date_consultation__gte=date_debut)
        except ValueError:
            pass
    
    # Filtre par date (fin)
    date_fin = request.GET.get('date_fin', '')
    if date_fin:
        try:
            date_fin = datetime.strptime(date_fin, '%Y-%m-%d')
            consultations = consultations.filter(date_consultation__lte=date_fin)
        except ValueError:
            pass
    
    # Pagination
    page = request.GET.get('page', 1)
    items_per_page = request.GET.get('per_page', 10)
    try:
        items_per_page = int(items_per_page)
        # Limiter les valeurs possibles
        if items_per_page not in [10, 25, 50, 100]:
            items_per_page = 10
    except (ValueError, TypeError):
        items_per_page = 10
    
    paginator = Paginator(consultations, items_per_page)
    
    try:
        consultations_page = paginator.page(page)
    except PageNotAnInteger:
        consultations_page = paginator.page(1)
    except EmptyPage:
        consultations_page = paginator.page(paginator.num_pages)
    
    context = {
        'consultations': consultations_page,
        'code_query': code_query,
        'patient_query': patient_query,
        'medecin_query': medecin_query,
        'date_debut': date_debut.strftime('%Y-%m-%d') if isinstance(date_debut, datetime) else '',
        'date_fin': date_fin.strftime('%Y-%m-%d') if isinstance(date_fin, datetime) else '',
        'per_page': items_per_page,
    }
    
    return render(request, 'koumaglo_consultations/consultation_list.html', context)

@login_required
def consultation_detail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    return render(request, 'koumaglo_consultations/consultation_detail.html', {'consultation': consultation})

@login_required
def consultation_add(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.utilisateur = request.user
            consultation.save()
            messages.success(request, "La consultation a été ajoutée avec succès.")
            return redirect('koumaglo_consultations:consultation_list')
    else:
        form = ConsultationForm()
    
    return render(request, 'koumaglo_consultations/consultation_form.html', {'form': form, 'mode': 'ajouter'})

@login_required
def consultation_edit(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    
    if request.method == 'POST':
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.utilisateur = request.user
            consultation.save()
            messages.success(request, "La consultation a été modifiée avec succès.")
            return redirect('koumaglo_consultations:consultation_detail', pk=consultation.pk)
    else:
        form = ConsultationForm(instance=consultation)
    
    return render(request, 'koumaglo_consultations/consultation_form.html', 
                  {'form': form, 'mode': 'modifier', 'consultation': consultation})

@login_required
def consultation_delete(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    
    if request.method == 'POST':
        consultation.delete()
        messages.success(request, "La consultation a été supprimée avec succès.")
        return redirect('koumaglo_consultations:consultation_list')
    
    return render(request, 'koumaglo_consultations/consultation_confirm_delete.html', {'consultation': consultation})
