from django.urls import path
from . import views

app_name = 'koumaglo_ordonnances'

urlpatterns = [
    path('ordonnances/', views.ordonnance_list, name='ordonnance_list'),
    path('ordonnances/ajouter/', views.ordonnance_add, name='ordonnance_add'),
    path('consultations/<int:consultation_id>/ordonnances/ajouter/', views.ordonnance_add, name='ordonnance_add_for_consultation'),
    path('ordonnances/<int:pk>/', views.ordonnance_detail, name='ordonnance_detail'),
    path('ordonnances/<int:pk>/modifier/', views.ordonnance_edit, name='ordonnance_edit'),
    path('ordonnances/<int:pk>/supprimer/', views.ordonnance_delete, name='ordonnance_delete'),
    path('ordonnances/<int:pk>/pdf/', views.ordonnance_pdf, name='ordonnance_pdf'),
] 