from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Medecin, Specialite, AffecterSpecialite
from .forms import SpecialiteForm, MedecinFormComplet
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

# Vues pour les médecins
@login_required
def medecin_list(request):
    medecins = Medecin.objects.all().order_by('personne__nom', 'personne__prenom')
    
    # Recherche textuelle (nom, prénom, titre)
    query = request.GET.get('query', '')
    if query:
        medecins = medecins.filter(
            Q(personne__nom__icontains=query) |
            Q(personne__prenom__icontains=query) |
            Q(titre_medecin__icontains=query)
        )
    
    # Filtrage par nom (maintenu pour compatibilité)
    nom_query = request.GET.get('nom', '')
    if nom_query:
        medecins = medecins.filter(personne__nom__icontains=nom_query)
    
    # Filtrage par spécialité
    specialite_id = request.GET.get('specialite', '')
    if specialite_id and specialite_id.isdigit():
        medecins = medecins.filter(affecterspecialite__specialite_id=specialite_id, affecterspecialite__actif=True).distinct()
    
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
    
    paginator = Paginator(medecins, items_per_page)
    
    try:
        medecins_page = paginator.page(page)
    except PageNotAnInteger:
        medecins_page = paginator.page(1)
    except EmptyPage:
        medecins_page = paginator.page(paginator.num_pages)
    
    # Liste des spécialités pour le formulaire de recherche
    specialites = Specialite.objects.all()
    
    return render(request, 'koumaglo_medecins/medecin_list.html', {
        'medecins': medecins_page, 
        'specialites': specialites,
        'nom_query': nom_query,
        'query': query,
        'specialite_id': specialite_id,
        'per_page': items_per_page
    })

@login_required
def medecin_detail(request, pk):
    medecin = get_object_or_404(Medecin, pk=pk)
    specialites = AffecterSpecialite.objects.filter(medecin=medecin, actif=True)
    return render(request, 'koumaglo_medecins/medecin_detail.html', 
                 {'medecin': medecin, 'specialites': specialites})

@login_required
def medecin_add(request):
    if request.method == 'POST':
        form = MedecinFormComplet(request.POST)
        if form.is_valid():
            # Gérer manuellement les spécialités
            specialite_ids = request.POST.getlist('specialites')
            form.cleaned_data['specialites'] = Specialite.objects.filter(id__in=specialite_ids)
            
            medecin = form.save()
            messages.success(request, "Le médecin a été ajouté avec succès.")
            return redirect('koumaglo_medecins:medecin_list')
    else:
        form = MedecinFormComplet()
    return render(request, 'koumaglo_medecins/medecin_form.html', {'form': form, 'mode': 'ajouter'})

@login_required
def medecin_edit(request, pk):
    medecin = get_object_or_404(Medecin, pk=pk)
    personne = medecin.personne
    
    if request.method == 'POST':
        form = MedecinFormComplet(request.POST)
        if form.is_valid():
            # On préserve le code de la personne existante
            form.cleaned_data['code'] = personne.code
            
            # Gérer manuellement les spécialités
            specialite_ids = request.POST.getlist('specialites')
            form.cleaned_data['specialites'] = Specialite.objects.filter(id__in=specialite_ids)
            
            medecin = form.save()
            messages.success(request, "Le médecin a été modifié avec succès.")
            return redirect('koumaglo_medecins:medecin_detail', pk=medecin.pk)
    else:
        # Prépopulation du formulaire sans les spécialités (gérées directement dans le template)
        initial_data = {
            'code': personne.code,
            'nom': personne.nom,
            'prenom': personne.prenom,
            'date_naissance': personne.date_naissance,
            'civilite': personne.civilite,
            'titre_medecin': medecin.titre_medecin,
        }
        
        form = MedecinFormComplet(initial=initial_data)
    
    return render(request, 'koumaglo_medecins/medecin_form.html', {'form': form, 'mode': 'modifier', 'medecin': medecin})

@login_required
def medecin_delete(request, pk):
    medecin = get_object_or_404(Medecin, pk=pk)
    
    if request.method == 'POST':
        # Supprimer le médecin et sa personne associée
        personne = medecin.personne
        medecin.delete()
        personne.delete()
        
        messages.success(request, "Le médecin a été supprimé avec succès.")
        return redirect('koumaglo_medecins:medecin_list')
    
    return render(request, 'koumaglo_medecins/medecin_confirm_delete.html', {'medecin': medecin})

# Vues pour les spécialités
@login_required
def specialite_list(request):
    specialites = Specialite.objects.all()
    return render(request, 'koumaglo_medecins/specialite_list.html', {'specialites': specialites})

@login_required
def specialite_add(request):
    if request.method == 'POST':
        form = SpecialiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('koumaglo_medecins:specialite_list')
    else:
        form = SpecialiteForm()
    return render(request, 'koumaglo_medecins/specialite_form.html', {'form': form, 'mode': 'ajouter'})

@login_required
def specialite_edit(request, pk):
    specialite = get_object_or_404(Specialite, pk=pk)
    if request.method == 'POST':
        form = SpecialiteForm(request.POST, instance=specialite)
        if form.is_valid():
            form.save()
            return redirect('koumaglo_medecins:specialite_list')
    else:
        form = SpecialiteForm(instance=specialite)
    return render(request, 'koumaglo_medecins/specialite_form.html', {'form': form, 'mode': 'modifier', 'specialite': specialite})

@login_required
def specialite_delete(request, pk):
    specialite = get_object_or_404(Specialite, pk=pk)
    if request.method == 'POST':
        specialite.delete()
        return redirect('koumaglo_medecins:specialite_list')
    return render(request, 'koumaglo_medecins/specialite_confirm_delete.html', {'specialite': specialite})
