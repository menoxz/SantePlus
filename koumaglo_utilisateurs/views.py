from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.contrib import messages
from koumaglo_patients.models import Patient
from koumaglo_medecins.models import Medecin
from koumaglo_consultations.models import Consultation
from koumaglo_factures.models import Facture
from django.utils import timezone
from datetime import timedelta
from .forms import UtilisateurProfilForm
from axes.models import AccessAttempt, AccessLog
from axes.utils import reset

# Create your views here.

# Fonction pour vérifier si l'utilisateur est administrateur
def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
def dashboard(request):
    # Statistiques générales
    stats = {
        'total_patients': Patient.objects.count(),
        'total_medecins': Medecin.objects.count(),
        'total_consultations': Consultation.objects.count(),
        'total_factures': Facture.objects.count(),
    }
    
    # Consultations récentes (derniers 30 jours)
    date_limite = timezone.now() - timedelta(days=30)
    consultations_recentes = Consultation.objects.filter(
        date_consultation__gte=date_limite
    ).order_by('-date_consultation')[:10]
    
    # Factures impayées
    factures_impayees = Facture.objects.filter(
        date_paiement_facture__isnull=True
    ).count()
    
    context = {
        'title': 'Tableau de Bord',
        'stats': stats,
        'consultations_recentes': consultations_recentes,
        'factures_impayees': factures_impayees,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def profil(request):
    if request.method == 'POST':
        form = UtilisateurProfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('koumaglo_utilisateurs:profil')
    else:
        form = UtilisateurProfilForm(instance=request.user)

    return render(request, 'koumaglo_utilisateurs/profil.html', {
        'title': 'Mon Profil',
        'user': request.user,
        'form': form
    })

@login_required
@user_passes_test(is_admin)
def view_login_attempts(request):
    # Récupérer les tentatives de connexion échouées
    failed_attempts = AccessAttempt.objects.all().order_by('-attempt_time')
    
    # Récupérer l'historique des connexions réussies
    successful_logins = AccessLog.objects.all().order_by('-attempt_time')[:50]
    
    context = {
        'title': 'Historique des tentatives de connexion',
        'failed_attempts': failed_attempts,
        'successful_logins': successful_logins,
    }
    
    return render(request, 'koumaglo_utilisateurs/login_attempts.html', context)

@login_required
@user_passes_test(is_admin)
def unlock_account(request, username):
    # Déverrouiller le compte de l'utilisateur
    reset(username=username)
    messages.success(request, f"Le compte de {username} a été déverrouillé avec succès.")
    return redirect('koumaglo_utilisateurs:login_attempts')
