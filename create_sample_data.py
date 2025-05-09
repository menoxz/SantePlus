import os
import sys
import django
import uuid
from django.utils import timezone
from datetime import date, timedelta

# Configuration pour utiliser les modèles Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'santeplus.settings')
django.setup()

# Import des modèles après la configuration Django
from koumaglo_parametres.models import Medicament, TypeActe, Acte
from koumaglo_patients.models import Patient, Personne
from koumaglo_medecins.models import Medecin, Specialite, AffecterSpecialite
from koumaglo_utilisateurs.models import Utilisateur

def create_sample_data():
    print("Création des données d'exemple...")
    
    # 1. Créer 5 médicaments
    medicaments = [
        {"libelle": "Paracétamol 500mg", "description": "Analgésique et antipyrétique pour douleurs légères à modérées"},
        {"libelle": "Amoxicilline 1g", "description": "Antibiotique à large spectre pour infections bactériennes"},
        {"libelle": "Ibuprofène 400mg", "description": "Anti-inflammatoire non stéroïdien (AINS) pour douleurs et inflammations"},
        {"libelle": "Oméprazole 20mg", "description": "Inhibiteur de la pompe à protons pour reflux gastro-œsophagien"},
        {"libelle": "Métformine 500mg", "description": "Antidiabétique oral pour le diabète de type 2"}
    ]
    
    for med_data in medicaments:
        Medicament.objects.get_or_create(
            libelle_medicament=med_data["libelle"],
            defaults={
                "description": med_data["description"],
                "code_medicament": f"MED{uuid.uuid4().hex[:8].upper()}"
            }
        )
    print("✅ 5 médicaments créés")
    
    # 2. Créer 5 types d'actes
    types_actes = [
        {"libelle": "Consultation standard", "description": "Consultation médicale de routine"},
        {"libelle": "Consultation spécialiste", "description": "Consultation avec un médecin spécialiste"},
        {"libelle": "Acte chirurgical mineur", "description": "Petite intervention chirurgicale"},
        {"libelle": "Imagerie médicale", "description": "Radiographie, échographie, etc."},
        {"libelle": "Analyse biologique", "description": "Prise de sang, analyse d'urine, etc."}
    ]
    
    for ta_data in types_actes:
        TypeActe.objects.get_or_create(
            libelle=ta_data["libelle"],
            defaults={
                "description": ta_data["description"],
                "code": f"TYP{uuid.uuid4().hex[:8].upper()}"
            }
        )
    print("✅ 5 types d'actes créés")
    
    # 3. Créer 5 actes médicaux
    actes = []
    types_actes = TypeActe.objects.all()[:5]
    specialites = Specialite.objects.all()[:5]
    
    actes_data = [
        {"libelle": "Consultation généraliste", "montant": 10000, "type_acte_index": 0, "specialite_index": 0},
        {"libelle": "Consultation cardiologue", "montant": 18000, "type_acte_index": 1, "specialite_index": 1},
        {"libelle": "Pansement simple", "montant": 5000, "type_acte_index": 2, "specialite_index": 2},
        {"libelle": "Échographie abdominale", "montant": 25000, "type_acte_index": 3, "specialite_index": 3},
        {"libelle": "Numération formule sanguine", "montant": 7500, "type_acte_index": 4, "specialite_index": 4}
    ]
    
    for acte_data in actes_data:
        if (types_actes.count() > acte_data["type_acte_index"] and 
            specialites.count() > acte_data["specialite_index"]):
            Acte.objects.get_or_create(
                libelle_acte=acte_data["libelle"],
                defaults={
                    "montant_acte": acte_data["montant"],
                    "type_acte": types_actes[acte_data["type_acte_index"]],
                    "specialite": specialites[acte_data["specialite_index"]],
                    "code_acte": f"ACT{uuid.uuid4().hex[:8].upper()}"
                }
            )
    print("✅ 5 actes médicaux créés")
    
    # 4. Créer 5 patients
    patients_data = [
        {"nom": "Dupont", "prenom": "Jean", "dob": date(1980, 5, 15), "civilite": "M"},
        {"nom": "Martin", "prenom": "Sophie", "dob": date(1992, 8, 23), "civilite": "F"},
        {"nom": "Dubois", "prenom": "Pierre", "dob": date(1976, 3, 10), "civilite": "M"},
        {"nom": "Laurent", "prenom": "Marie", "dob": date(1988, 11, 7), "civilite": "F"},
        {"nom": "Lefebvre", "prenom": "Thomas", "dob": date(1995, 1, 30), "civilite": "M"}
    ]
    
    for pat_data in patients_data:
        # Créer la personne
        personne, created = Personne.objects.get_or_create(
            nom=pat_data["nom"],
            prenom=pat_data["prenom"],
            defaults={
                "date_naissance": pat_data["dob"],
                "civilite": pat_data["civilite"],
                "code": f"P{uuid.uuid4().hex[:8].upper()}"
            }
        )
        
        # Créer le patient associé s'il n'existe pas déjà
        if created or not Patient.objects.filter(personne=personne).exists():
            Patient.objects.create(
                personne=personne,
                date_enreg=timezone.now()
            )
    print("✅ 5 patients créés")
    
    # 5. Créer 5 médecins
    # D'abord, créer quelques spécialités
    specialites_data = [
        {"libelle": "Médecine générale"},
        {"libelle": "Cardiologie"},
        {"libelle": "Pédiatrie"},
        {"libelle": "Dermatologie"},
        {"libelle": "Gynécologie"}
    ]
    
    specialites = []
    for spec_data in specialites_data:
        specialite, _ = Specialite.objects.get_or_create(
            libelle=spec_data["libelle"],
            defaults={"code": f"SPE{uuid.uuid4().hex[:8].upper()}"}
        )
        specialites.append(specialite)
    
    # Créer les médecins
    medecins_data = [
        {"nom": "Bernard", "prenom": "Alain", "dob": date(1975, 6, 20), "civilite": "M", "titre": "Dr.", "specialite_index": 0},
        {"nom": "Robert", "prenom": "Émilie", "dob": date(1982, 9, 12), "civilite": "F", "titre": "Dr.", "specialite_index": 1},
        {"nom": "Moreau", "prenom": "François", "dob": date(1968, 4, 5), "civilite": "M", "titre": "Dr.", "specialite_index": 2},
        {"nom": "Petit", "prenom": "Isabelle", "dob": date(1978, 7, 28), "civilite": "F", "titre": "Dr.", "specialite_index": 3},
        {"nom": "Simon", "prenom": "Michel", "dob": date(1972, 2, 17), "civilite": "M", "titre": "Pr.", "specialite_index": 4}
    ]
    
    for med_data in medecins_data:
        # Créer la personne
        personne, created_personne = Personne.objects.get_or_create(
            nom=med_data["nom"],
            prenom=med_data["prenom"],
            defaults={
                "date_naissance": med_data["dob"],
                "civilite": med_data["civilite"],
                "code": f"M{uuid.uuid4().hex[:8].upper()}"
            }
        )
        
        # Créer le médecin
        if created_personne or not Medecin.objects.filter(personne=personne).exists():
            medecin = Medecin.objects.create(
                personne=personne,
                titre_medecin=med_data["titre"]
            )
            
            # Associer à la spécialité via AffecterSpecialite
            if len(specialites) > med_data["specialite_index"]:
                specialite = specialites[med_data["specialite_index"]]
                AffecterSpecialite.objects.create(
                    medecin=medecin,
                    specialite=specialite,
                    date_affectation=timezone.now(),
                    actif=True
                )
    
    print("✅ 5 médecins créés")
    print("\nToutes les données d'exemple ont été créées avec succès!")

if __name__ == "__main__":
    create_sample_data()