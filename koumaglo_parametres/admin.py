from django.contrib import admin
from .models import Medicament, TypeActe, Acte

@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    list_display = ('code_medicament', 'libelle_medicament')
    search_fields = ('code_medicament', 'libelle_medicament')
    list_filter = ('date_creation',)

@admin.register(TypeActe)
class TypeActeAdmin(admin.ModelAdmin):
    list_display = ('code', 'libelle')
    search_fields = ('code', 'libelle')
    list_filter = ('date_creation',)

@admin.register(Acte)
class ActeAdmin(admin.ModelAdmin):
    list_display = ('code_acte', 'libelle_acte', 'montant_acte', 'type_acte', 'specialite', 'consultation')
    search_fields = ('code_acte', 'libelle_acte')
    list_filter = ('type_acte', 'specialite')
