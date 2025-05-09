from django.db import migrations
from django.db.models import F, Q

def fill_acte_specialite(apps, schema_editor):
    """
    Cette fonction assigne une spécialité aux actes existants basés sur les spécialités des médecins
    des consultations auxquelles ils sont liés.
    """
    Acte = apps.get_model('koumaglo_parametres', 'Acte')
    Specialite = apps.get_model('koumaglo_medecins', 'Specialite')
    AffecterSpecialite = apps.get_model('koumaglo_medecins', 'AffecterSpecialite')
    
    # Pour les actes liés à une consultation
    actes_avec_consultation = Acte.objects.filter(consultation__isnull=False, specialite__isnull=True)
    
    for acte in actes_avec_consultation:
        # Trouver les spécialités du médecin de la consultation
        medecin = acte.consultation.medecin
        specialites = AffecterSpecialite.objects.filter(medecin=medecin, actif=True)
        
        if specialites.exists():
            # Prendre la première spécialité active du médecin
            acte.specialite = specialites.first().specialite
            acte.save()
    
    # Pour les actes sans consultation, essayer de leur attribuer une spécialité
    # basée sur leur type d'acte et les spécialités existantes
    actes_sans_specialite = Acte.objects.filter(specialite__isnull=True)
    
    # Prendre la première spécialité disponible comme valeur par défaut
    specialite_par_defaut = Specialite.objects.first()
    
    if specialite_par_defaut:
        # Mettre à jour tous les actes sans spécialité
        actes_sans_specialite.update(specialite=specialite_par_defaut)

class Migration(migrations.Migration):
    dependencies = [
        ('koumaglo_parametres', '0003_remove_typeacte_specialites_acte_specialite'),
    ]

    operations = [
        migrations.RunPython(fill_acte_specialite, migrations.RunPython.noop),
    ] 