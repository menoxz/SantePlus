from django.urls import path
from . import views

app_name = 'koumaglo_patients'

urlpatterns = [
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.patient_add, name='patient_add'),
    path('patients/edit/<int:pk>/', views.patient_edit, name='patient_edit'),
    path('patients/delete/<int:pk>/', views.patient_delete, name='patient_delete'),
    path('patients/recherche/', views.patient_search, name='patient_search'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
] 