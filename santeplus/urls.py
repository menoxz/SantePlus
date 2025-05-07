"""
URL configuration for santeplus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('koumaglo_utilisateurs.urls', namespace='koumaglo_utilisateurs')),
    path('', include('koumaglo_patients.urls', namespace='koumaglo_patients')),
    path('', include('koumaglo_medecins.urls', namespace='koumaglo_medecins')),
    path('', include('koumaglo_consultations.urls', namespace='koumaglo_consultations')),
    path('', include('koumaglo_ordonnances.urls', namespace='koumaglo_ordonnances')),
    path('', include('koumaglo_factures.urls', namespace='koumaglo_factures')),
    path('parametres/', include('koumaglo_parametres.urls', namespace='koumaglo_parametres')),
    path('', lambda request: redirect('koumaglo_utilisateurs:login'), name='root'),
]
