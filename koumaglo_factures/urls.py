from django.urls import path
from . import views

app_name = 'koumaglo_factures'

urlpatterns = [
    # Vue de liste des factures
    path('', views.facture_list, name='facture_list'),
    
    # Sélection du patient et de la consultation pour créer une facture
    path('selectionner-patient/', views.select_patient_for_facture, name='select_patient'),
    path('selectionner-consultation/<int:patient_id>/', views.select_consultation, name='select_consultation'),
    path('apercu-facture/<int:consultation_id>/', views.facture_preview, name='facture_preview'),
    
    # Détails, modification et suppression d'une facture
    path('<int:pk>/', views.facture_detail, name='facture_detail'),
    path('<int:pk>/modifier/', views.facture_edit, name='facture_edit'),
    path('<int:pk>/supprimer/', views.facture_delete, name='facture_delete'),
    
    # Génération de PDF
    path('<int:pk>/pdf/', views.facture_pdf, name='facture_pdf'),
    
    # API pour récupérer le montant d'un acte
    path('api/acte-montant/<int:acte_id>/', views.get_acte_montant, name='get_acte_montant'),
] 