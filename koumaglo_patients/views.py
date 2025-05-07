from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient, Personne
from .forms import PatientFormComplet
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

@login_required
def patient_list(request):
    patients = Patient.objects.all().order_by('personne__nom', 'personne__prenom')
    
    # Recherche par nom ou prénom
    query = request.GET.get('q', '')
    if query:
        patients = patients.filter(
            Q(personne__nom__icontains=query) | 
            Q(personne__prenom__icontains=query)
        )
    
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
    
    paginator = Paginator(patients, items_per_page)
    
    try:
        patients_page = paginator.page(page)
    except PageNotAnInteger:
        patients_page = paginator.page(1)
    except EmptyPage:
        patients_page = paginator.page(paginator.num_pages)
    
    context = {
        'patients': patients_page,
        'query': query,
        'per_page': items_per_page
    }
    
    return render(request, 'koumaglo_patients/patient_list.html', context)

@login_required
def patient_add(request):
    if request.method == 'POST':
        form = PatientFormComplet(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect('koumaglo_patients:patient_list')
    else:
        form = PatientFormComplet()
    return render(request, 'koumaglo_patients/patient_add.html', {'form': form})

@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    personne = patient.personne
    
    if request.method == 'POST':
        form = PatientFormComplet(request.POST)
        if form.is_valid():
            # Nous préservons la personne existante mais mettons à jour ses attributs
            form.cleaned_data['code'] = personne.code  # Conserver le même code
            patient = form.save()
            return redirect('koumaglo_patients:patient_list')
    else:
        # Pré-remplir le formulaire avec les données existantes
        form = PatientFormComplet(initial={
            'code': personne.code,
            'nom': personne.nom,
            'prenom': personne.prenom,
            'date_naissance': personne.date_naissance,
            'civilite': personne.civilite
        })
    return render(request, 'koumaglo_patients/patient_edit.html', {'form': form, 'patient': patient})

@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        # Supprimer la personne associée supprime aussi le patient grâce à CASCADE
        patient.personne.delete()
        return redirect('koumaglo_patients:patient_list')
    return render(request, 'koumaglo_patients/patient_delete.html', {'patient': patient})

@login_required
def patient_search(request):
    query = request.GET.get('q', '')
    
    if query:
        patients = Patient.objects.filter(
            Q(personne__nom__icontains=query) | 
            Q(personne__prenom__icontains=query)
        ).order_by('personne__nom', 'personne__prenom')
    else:
        patients = Patient.objects.all().order_by('personne__nom', 'personne__prenom')
    
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
    
    paginator = Paginator(patients, items_per_page)
    
    try:
        patients_page = paginator.page(page)
    except PageNotAnInteger:
        patients_page = paginator.page(1)
    except EmptyPage:
        patients_page = paginator.page(paginator.num_pages)
    
    context = {
        'patients': patients_page,
        'query': query,
        'per_page': items_per_page
    }
    
    return render(request, 'koumaglo_patients/patient_list.html', context)

#detail patient
@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'koumaglo_patients/patient_detail.html', {'patient': patient})

