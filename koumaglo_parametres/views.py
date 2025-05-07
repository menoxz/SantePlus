from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Medicament, TypeActe, Acte
from .forms import MedicamentForm, TypeActeForm, ActeForm

# Create your views here.

# Vues pour les médicaments
@login_required
def medicament_list(request):
    search_query = request.GET.get('search', '')
    medicaments = Medicament.objects.all()
    
    if search_query:
        medicaments = medicaments.filter(
            Q(libelle_medicament__icontains=search_query) |
            Q(code_medicament__icontains=search_query)
        )
    
    context = {
        'medicaments': medicaments,
        'search_query': search_query
    }
    return render(request, 'koumaglo_parametres/medicament_list.html', context)

@login_required
def medicament_add(request):
    if request.method == 'POST':
        form = MedicamentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Médicament ajouté avec succès.')
            return redirect('koumaglo_parametres:medicament_list')
    else:
        form = MedicamentForm()
    
    return render(request, 'koumaglo_parametres/medicament_form.html', {'form': form, 'title': 'Ajouter un médicament'})

@login_required
def medicament_edit(request, pk):
    medicament = get_object_or_404(Medicament, pk=pk)
    if request.method == 'POST':
        form = MedicamentForm(request.POST, instance=medicament)
        if form.is_valid():
            form.save()
            messages.success(request, 'Médicament modifié avec succès.')
            return redirect('koumaglo_parametres:medicament_list')
    else:
        form = MedicamentForm(instance=medicament)
    
    return render(request, 'koumaglo_parametres/medicament_form.html', {'form': form, 'title': 'Modifier un médicament'})

@login_required
def medicament_delete(request, pk):
    medicament = get_object_or_404(Medicament, pk=pk)
    if request.method == 'POST':
        medicament.delete()
        messages.success(request, 'Médicament supprimé avec succès.')
        return redirect('koumaglo_parametres:medicament_list')
    return render(request, 'koumaglo_parametres/medicament_confirm_delete.html', {'medicament': medicament})

# Vues pour les types d'actes
@login_required
def type_acte_list(request):
    search_query = request.GET.get('search', '')
    types_actes = TypeActe.objects.all()
    
    if search_query:
        types_actes = types_actes.filter(
            Q(libelle__icontains=search_query) |
            Q(code__icontains=search_query)
        )
    
    context = {
        'types_actes': types_actes,
        'search_query': search_query
    }
    return render(request, 'koumaglo_parametres/type_acte_list.html', context)

@login_required
def type_acte_add(request):
    if request.method == 'POST':
        form = TypeActeForm(request.POST)
        if form.is_valid():
            type_acte = form.save()
            # Gérer les spécialités sélectionnées
            specialites = form.cleaned_data.get('specialites')
            if specialites:
                type_acte.specialites.set(specialites)
            messages.success(request, 'Type d\'acte ajouté avec succès.')
            return redirect('koumaglo_parametres:type_acte_list')
    else:
        form = TypeActeForm()
    
    return render(request, 'koumaglo_parametres/type_acte_form.html', {'form': form, 'title': 'Ajouter un type d\'acte'})

@login_required
def type_acte_edit(request, pk):
    type_acte = get_object_or_404(TypeActe, pk=pk)
    if request.method == 'POST':
        form = TypeActeForm(request.POST, instance=type_acte)
        if form.is_valid():
            type_acte = form.save()
            # Gérer les spécialités sélectionnées
            specialites = form.cleaned_data.get('specialites')
            type_acte.specialites.set(specialites)
            messages.success(request, 'Type d\'acte modifié avec succès.')
            return redirect('koumaglo_parametres:type_acte_list')
    else:
        form = TypeActeForm(instance=type_acte)
        # Préremplir les spécialités
        form.fields['specialites'].initial = type_acte.specialites.all()
    
    return render(request, 'koumaglo_parametres/type_acte_form.html', {'form': form, 'title': 'Modifier un type d\'acte'})

@login_required
def type_acte_delete(request, pk):
    type_acte = get_object_or_404(TypeActe, pk=pk)
    if request.method == 'POST':
        type_acte.delete()
        messages.success(request, 'Type d\'acte supprimé avec succès.')
        return redirect('koumaglo_parametres:type_acte_list')
    return render(request, 'koumaglo_parametres/type_acte_confirm_delete.html', {'type_acte': type_acte})

# Vues pour les actes
@login_required
def acte_list(request):
    search_query = request.GET.get('search', '')
    actes = Acte.objects.all()
    
    if search_query:
        actes = actes.filter(
            Q(libelle_acte__icontains=search_query) |
            Q(code_acte__icontains=search_query)
        )
    
    context = {
        'actes': actes,
        'search_query': search_query
    }
    return render(request, 'koumaglo_parametres/acte_list.html', context)

@login_required
def acte_add(request):
    consultation_id = request.GET.get('consultation')
    
    if request.method == 'POST':
        form = ActeForm(request.POST, consultation_id=consultation_id)
        if form.is_valid():
            acte = form.save()
            messages.success(request, 'Acte ajouté avec succès.')
            
            # Rediriger vers les détails de la consultation si l'acte est lié à une consultation
            if acte.consultation:
                return redirect('koumaglo_consultations:consultation_detail', pk=acte.consultation.pk)
            return redirect('koumaglo_parametres:acte_list')
    else:
        form = ActeForm(consultation_id=consultation_id)
    
    return render(request, 'koumaglo_parametres/acte_form.html', {'form': form, 'title': 'Ajouter un acte'})

@login_required
def acte_edit(request, pk):
    acte = get_object_or_404(Acte, pk=pk)
    consultation_id = acte.consultation.id if acte.consultation else None
    
    if request.method == 'POST':
        form = ActeForm(request.POST, instance=acte, consultation_id=consultation_id)
        if form.is_valid():
            acte = form.save()
            messages.success(request, 'Acte modifié avec succès.')
            
            # Rediriger vers les détails de la consultation si l'acte est lié à une consultation
            if acte.consultation:
                return redirect('koumaglo_consultations:consultation_detail', pk=acte.consultation.pk)
            return redirect('koumaglo_parametres:acte_list')
    else:
        form = ActeForm(instance=acte, consultation_id=consultation_id)
    
    return render(request, 'koumaglo_parametres/acte_form.html', {'form': form, 'title': 'Modifier un acte'})

@login_required
def acte_delete(request, pk):
    acte = get_object_or_404(Acte, pk=pk)
    consultation = acte.consultation
    
    if request.method == 'POST':
        acte.delete()
        messages.success(request, 'Acte supprimé avec succès.')
        
        # Rediriger vers les détails de la consultation si l'acte était lié à une consultation
        if consultation:
            return redirect('koumaglo_consultations:consultation_detail', pk=consultation.pk)
        return redirect('koumaglo_parametres:acte_list')
    
    return render(request, 'koumaglo_parametres/acte_confirm_delete.html', {'acte': acte})
