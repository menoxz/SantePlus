from django.db import models
from koumaglo_patients.models import Personne

# Create your models here.

class Specialite(models.Model):
    code = models.CharField(max_length=50, unique=True)
    libelle = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Spécialité'
        verbose_name_plural = 'Spécialités'

    def __str__(self):
        return self.libelle

class Medecin(models.Model):
    personne = models.OneToOneField(Personne, on_delete=models.CASCADE, primary_key=True)
    titre_medecin = models.CharField(max_length=50)
    specialites = models.ManyToManyField(Specialite, through='AffecterSpecialite')

    class Meta:
        verbose_name = 'Médecin'
        verbose_name_plural = 'Médecins'

    def __str__(self):
        return f'Dr. {self.personne.nom} {self.personne.prenom}'

class AffecterSpecialite(models.Model):
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE)
    date_affectation = models.DateField()
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Affectation Spécialité'
        verbose_name_plural = 'Affectations Spécialités'

    def __str__(self):
        return f'{self.medecin} - {self.specialite} ({self.date_affectation})'
