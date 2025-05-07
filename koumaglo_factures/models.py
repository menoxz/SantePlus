from django.db import models
from koumaglo_consultations.models import Consultation
from koumaglo_medecins.models import Medecin
from koumaglo_utilisateurs.models import Utilisateur
from koumaglo_parametres.models import Acte

class Facture(models.Model):
    code_facture = models.CharField(max_length=50, unique=True)
    type_facture = models.CharField(max_length=50)
    date_enreg_facture = models.DateTimeField(auto_now_add=True)
    date_paiement_facture = models.DateTimeField(null=True, blank=True)
    montant_facture = models.DecimalField(max_digits=10, decimal_places=2)
    montant_paye_facture = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='factures')
    medecin = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, blank=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Facture'
        verbose_name_plural = 'Factures'

    def __str__(self):
        return f'Facture {self.code_facture} - {self.montant_facture} FCFA'

class FactureDetail(models.Model):
    code_detail_facture = models.CharField(max_length=50, unique=True)
    montant_facture_detail = models.DecimalField(max_digits=10, decimal_places=2)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='details')
    acte = models.ForeignKey(Acte, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Détail Facture'
        verbose_name_plural = 'Détails Factures'

    def __str__(self):
        return f'Détail {self.code_detail_facture} - {self.acte}'

class Paiement(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paymentDate = models.DateTimeField()
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='paiements')

    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'

    def __str__(self):
        return f'Paiement de {self.amount} FCFA le {self.paymentDate}'
