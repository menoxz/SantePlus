from django.db import models

# Create your models here.

class Personne(models.Model):
    code = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    civilite = models.CharField(max_length=20, choices=[('M', 'Monsieur'), ('Mme', 'Madame'), ('Mlle', 'Mademoiselle')])

    class Meta:
        verbose_name = 'Personne'
        verbose_name_plural = 'Personnes'

    def __str__(self):
        return f'{self.nom} {self.prenom}'

class Patient(models.Model):
    personne = models.OneToOneField(Personne, on_delete=models.CASCADE, primary_key=True)
    date_enreg = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        return str(self.personne)
