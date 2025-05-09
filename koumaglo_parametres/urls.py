from django.urls import path
from . import views

app_name = 'koumaglo_parametres'

urlpatterns = [
    # URLs pour les médicaments
    path('medicaments/', views.medicament_list, name='medicament_list'),
    path('medicaments/ajouter/', views.medicament_add, name='medicament_add'),
    path('medicaments/<int:pk>/modifier/', views.medicament_edit, name='medicament_edit'),
    path('medicaments/<int:pk>/supprimer/', views.medicament_delete, name='medicament_delete'),
    
    # URLs pour les types d'actes
    path('types-actes/', views.type_acte_list, name='type_acte_list'),
    path('types-actes/ajouter/', views.type_acte_add, name='type_acte_add'),
    path('types-actes/<int:pk>/modifier/', views.type_acte_edit, name='type_acte_edit'),
    path('types-actes/<int:pk>/supprimer/', views.type_acte_delete, name='type_acte_delete'),

    # URLs pour les actes
    path('actes/', views.acte_list, name='acte_list'),
    path('actes/ajouter/', views.acte_add, name='acte_add'),
    path('actes/<int:pk>/modifier/', views.acte_edit, name='acte_edit'),
    path('actes/<int:pk>/supprimer/', views.acte_delete, name='acte_delete'),
    path('actes/affecter-consultation/', views.acte_affecter_consultation, name='acte_affecter_consultation'),
] 