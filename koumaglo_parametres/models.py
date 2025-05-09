from django.db import models
from django.utils import timezone
import uuid
from koumaglo_medecins.models import Specialite

# Create your models here.

class Medicament(models.Model):
    code_medicament = models.CharField(max_length=50, unique=True)
    libelle_medicament = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['libelle_medicament']
        verbose_name = 'Médicament'
        verbose_name_plural = 'Médicaments'

    def __str__(self):
        return self.libelle_medicament
        
    def save(self, *args, **kwargs):
        if not self.code_medicament:
            self.code_medicament = f"MED{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class TypeActe(models.Model):
    code = models.CharField(max_length=50, unique=True)
    libelle = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['libelle']
        verbose_name = 'Type d\'acte'
        verbose_name_plural = 'Types d\'actes'

    def __str__(self):
        return self.libelle
        
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"TYP{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class Acte(models.Model):
    code_acte = models.CharField(max_length=50, unique=True)
    libelle_acte = models.CharField(max_length=100)
    montant_acte = models.DecimalField(max_digits=10, decimal_places=2)
    type_acte = models.ForeignKey(TypeActe, on_delete=models.CASCADE, related_name='actes')
    specialite = models.ForeignKey('koumaglo_medecins.Specialite', on_delete=models.CASCADE, related_name='actes', null=True)
    consultation = models.ForeignKey('koumaglo_consultations.Consultation', on_delete=models.CASCADE, related_name='actes', null=True, blank=True)

    class Meta:
        verbose_name = 'Acte'
        verbose_name_plural = 'Actes'

    def __str__(self):
        return f'{self.libelle_acte} ({self.montant_acte} FCFA)'
        
    def save(self, *args, **kwargs):
        if not self.code_acte:
            self.code_acte = f"ACT{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
