from django.db import models
from koumaglo_patients.models import Patient
from koumaglo_medecins.models import Medecin
from koumaglo_utilisateurs.models import Utilisateur

class Consultation(models.Model):
    code_consultation = models.CharField(max_length=50, unique=True)
    date_consultation = models.DateTimeField()
    date_fin_validite_consultation = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Consultation'
        verbose_name_plural = 'Consultations'

    def __str__(self):
        return f'Consultation {self.code_consultation} - {self.patient} avec {self.medecin}'
