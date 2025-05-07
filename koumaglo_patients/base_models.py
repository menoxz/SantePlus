from django.db import models

class BasePersonne(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    civilite = models.CharField(max_length=20, choices=[('M', 'Monsieur'), ('Mme', 'Madame'), ('Mlle', 'Mademoiselle')])

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.nom} {self.prenom}' 