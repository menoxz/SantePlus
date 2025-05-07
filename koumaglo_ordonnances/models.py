from django.db import models
from koumaglo_consultations.models import Consultation

# Create your models here.

class Ordonnance(models.Model):
    code_ordonnance = models.CharField(max_length=50, unique=True)
    date_ordonnance = models.DateTimeField()
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='ordonnances')

    class Meta:
        verbose_name = 'Ordonnance'
        verbose_name_plural = 'Ordonnances'

    def __str__(self):
        return f'Ordonnance {self.code_ordonnance} - {self.date_ordonnance}'

class OrdonnanceDetail(models.Model):
    code_ordonnance_detail = models.CharField(max_length=50, unique=True)
    posologie_medicament = models.TextField()
    ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE, related_name='details')
    medicament = models.ForeignKey('koumaglo_parametres.Medicament', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Détail Ordonnance'
        verbose_name_plural = 'Détails Ordonnances'

    def __str__(self):
        return f'Détail {self.code_ordonnance_detail} - {self.medicament}'
