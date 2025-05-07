from django.urls import path
from . import views

app_name = 'koumaglo_consultations'

urlpatterns = [
    path('consultations/', views.consultation_list, name='consultation_list'),
    path('consultations/ajouter/', views.consultation_add, name='consultation_add'),
    path('consultations/<int:pk>/', views.consultation_detail, name='consultation_detail'),
    path('consultations/<int:pk>/modifier/', views.consultation_edit, name='consultation_edit'),
    path('consultations/<int:pk>/supprimer/', views.consultation_delete, name='consultation_delete'),
] 