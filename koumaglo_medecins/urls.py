from django.urls import path
from . import views

app_name = 'koumaglo_medecins'

urlpatterns = [
    path('medecins/', views.medecin_list, name='medecin_list'),
    path('medecins/ajouter/', views.medecin_add, name='medecin_add'),
    path('medecins/<int:pk>/', views.medecin_detail, name='medecin_detail'),
    path('medecins/<int:pk>/modifier/', views.medecin_edit, name='medecin_edit'),
    path('medecins/<int:pk>/supprimer/', views.medecin_delete, name='medecin_delete'),
    path('specialites/', views.specialite_list, name='specialite_list'),
    path('specialites/ajouter/', views.specialite_add, name='specialite_add'),
    path('specialites/<int:pk>/modifier/', views.specialite_edit, name='specialite_edit'),
    path('specialites/<int:pk>/supprimer/', views.specialite_delete, name='specialite_delete'),
] 