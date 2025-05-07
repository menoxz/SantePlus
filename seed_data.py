import os
import django
import random
from datetime import datetime, timedelta
import uuid

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'santeplus.settings')
django.setup()

# Import après configuration Django
from faker import Faker
from django.contrib.auth import get_user_model
from koumaglo_utilisateurs.models import Utilisateur
from koumaglo_patients.models import Patient, Personne
from koumaglo_medecins.models import Medecin, Specialite, AffecterSpecialite
from koumaglo_parametres.models import TypeActe, Medicament
from koumaglo_consultations.models import Consultation

Utilisateur = get_user_model()

# Initialisation de Faker en français
fake = Faker(['fr_FR'])
Faker.seed(42)  # Pour la reproductibilité

# Nettoyage de la base de données
def clear_data():
    print("Suppression des données existantes...")
    # Suppression en respectant les dépendances
    Consultation.objects.all().delete()
    AffecterSpecialite.objects.all().delete()
    TypeActe.objects.all().delete()
    Medicament.objects.all().delete()
    Patient.objects.all().delete()
    Medecin.objects.all().delete()
    Personne.objects.all().delete()
    Specialite.objects.all().delete()
    # Ne pas supprimer les utilisateurs administrateurs
    Utilisateur.objects.filter(is_superuser=False, is_staff=False).delete()
    print("Données existantes supprimées.")

# Création de l'utilisateur administrateur
def create_admin_user():
    if not Utilisateur.objects.filter(username='admin').exists():
        admin = Utilisateur.objects.create_superuser(
            username='admin',
            email='admin@santeplus.com',
            password='admin123',
            first_name='Administrateur',
            last_name='Système'
        )
        print(f"Utilisateur administrateur créé: {admin.username}")
    else:
        print("L'utilisateur administrateur existe déjà.")
    return Utilisateur.objects.get(username='admin')

# Création des spécialités médicales
def create_specialites():
    specialites = [
        {"code": "CARD", "libelle": "Cardiologie"},
        {"code": "DERM", "libelle": "Dermatologie"},
        {"code": "GAST", "libelle": "Gastro-entérologie"},
        {"code": "GYNE", "libelle": "Gynécologie"},
        {"code": "NEUR", "libelle": "Neurologie"},
        {"code": "OPHT", "libelle": "Ophtalmologie"},
        {"code": "ORTH", "libelle": "Orthopédie"},
        {"code": "ORL", "libelle": "Oto-rhino-laryngologie"},
        {"code": "PEDI", "libelle": "Pédiatrie"},
        {"code": "PSYC", "libelle": "Psychiatrie"},
        {"code": "RADI", "libelle": "Radiologie"},
        {"code": "UROL", "libelle": "Urologie"},
        {"code": "ANES", "libelle": "Anesthésiologie"},
        {"code": "GENT", "libelle": "Médecine générale"},
        {"code": "MINT", "libelle": "Médecine interne"},
    ]
    
    created_specialites = []
    for specialite_data in specialites:
        specialite, created = Specialite.objects.get_or_create(
            code=specialite_data["code"],
            defaults={"libelle": specialite_data["libelle"]}
        )
        created_specialites.append(specialite)
        if created:
            print(f"Spécialité créée: {specialite.libelle}")
        else:
            print(f"Spécialité existante: {specialite.libelle}")
    
    return created_specialites

# Création des types d'actes médicaux
def create_types_actes(specialites):
    types_actes = [
        {"libelle": "Consultation standard", "description": "Consultation médicale de base", "specialites": ["Médecine générale", "Médecine interne"]},
        {"libelle": "Électrocardiogramme (ECG)", "description": "Enregistrement de l'activité électrique du cœur", "specialites": ["Cardiologie"]},
        {"libelle": "Échographie cardiaque", "description": "Examen du cœur par ultrasons", "specialites": ["Cardiologie"]},
        {"libelle": "Biopsie cutanée", "description": "Prélèvement d'un échantillon de peau pour analyse", "specialites": ["Dermatologie"]},
        {"libelle": "Cryothérapie", "description": "Traitement par le froid de lésions cutanées", "specialites": ["Dermatologie"]},
        {"libelle": "Endoscopie digestive", "description": "Examen visuel du tractus digestif", "specialites": ["Gastro-entérologie"]},
        {"libelle": "Coloscopie", "description": "Examen du côlon par endoscopie", "specialites": ["Gastro-entérologie"]},
        {"libelle": "Examen gynécologique", "description": "Examen des organes génitaux féminins", "specialites": ["Gynécologie"]},
        {"libelle": "Frottis cervico-vaginal", "description": "Prélèvement pour dépistage du cancer du col de l'utérus", "specialites": ["Gynécologie"]},
        {"libelle": "Électroencéphalogramme (EEG)", "description": "Enregistrement de l'activité électrique du cerveau", "specialites": ["Neurologie"]},
        {"libelle": "Ponction lombaire", "description": "Prélèvement de liquide céphalo-rachidien", "specialites": ["Neurologie"]},
        {"libelle": "Fond d'œil", "description": "Examen de la rétine", "specialites": ["Ophtalmologie"]},
        {"libelle": "Tonométrie", "description": "Mesure de la pression intraoculaire", "specialites": ["Ophtalmologie"]},
        {"libelle": "Radiographie osseuse", "description": "Imagerie des os par rayons X", "specialites": ["Orthopédie", "Radiologie"]},
        {"libelle": "Infiltration articulaire", "description": "Injection de médicament dans une articulation", "specialites": ["Orthopédie"]},
        {"libelle": "Audiométrie", "description": "Test de l'audition", "specialites": ["Oto-rhino-laryngologie"]},
        {"libelle": "Examen ORL complet", "description": "Examen des oreilles, du nez et de la gorge", "specialites": ["Oto-rhino-laryngologie"]},
        {"libelle": "Consultation pédiatrique", "description": "Consultation médicale pour enfant", "specialites": ["Pédiatrie"]},
        {"libelle": "Évaluation du développement", "description": "Évaluation du développement physique et psychomoteur de l'enfant", "specialites": ["Pédiatrie"]},
        {"libelle": "Entretien psychiatrique", "description": "Consultation en psychiatrie", "specialites": ["Psychiatrie"]},
        {"libelle": "Psychothérapie", "description": "Séance de thérapie psychologique", "specialites": ["Psychiatrie"]},
        {"libelle": "Échographie abdominale", "description": "Examen de l'abdomen par ultrasons", "specialites": ["Radiologie", "Gastro-entérologie"]},
        {"libelle": "Scanner (TDM)", "description": "Tomodensitométrie par ordinateur", "specialites": ["Radiologie"]},
        {"libelle": "Cystoscopie", "description": "Examen de la vessie par endoscopie", "specialites": ["Urologie"]},
        {"libelle": "Bilan urodynamique", "description": "Évaluation du fonctionnement de l'appareil urinaire", "specialites": ["Urologie"]},
        {"libelle": "Consultation préopératoire", "description": "Évaluation avant une opération", "specialites": ["Anesthésiologie"]},
        {"libelle": "Anesthésie locale", "description": "Anesthésie limitée à une zone du corps", "specialites": ["Anesthésiologie", "Dermatologie"]},
    ]
    
    created_types_actes = []
    for acte_data in types_actes:
        type_acte, created = TypeActe.objects.get_or_create(
            libelle=acte_data["libelle"],
            defaults={"description": acte_data["description"]}
        )
        
        # Associer aux spécialités
        for specialite_name in acte_data["specialites"]:
            try:
                specialite = Specialite.objects.get(libelle=specialite_name)
                type_acte.specialites.add(specialite)
            except Specialite.DoesNotExist:
                print(f"Spécialité non trouvée: {specialite_name}")
        
        created_types_actes.append(type_acte)
        if created:
            print(f"Type d'acte créé: {type_acte.libelle}")
        else:
            print(f"Type d'acte existant: {type_acte.libelle}")
    
    return created_types_actes

# Création des médicaments
def create_medicaments():
    medicaments = [
        {"libelle": "Paracétamol", "description": "Analgésique et antipyrétique"},
        {"libelle": "Ibuprofène", "description": "Anti-inflammatoire non stéroïdien"},
        {"libelle": "Amoxicilline", "description": "Antibiotique de la famille des pénicillines"},
        {"libelle": "Oméprazole", "description": "Inhibiteur de la pompe à protons, réducteur d'acidité gastrique"},
        {"libelle": "Lévothyroxine", "description": "Hormone thyroïdienne synthétique"},
        {"libelle": "Amlodipine", "description": "Antihypertenseur, inhibiteur calcique"},
        {"libelle": "Salbutamol", "description": "Bronchodilatateur pour l'asthme"},
        {"libelle": "Metformine", "description": "Antidiabétique oral"},
        {"libelle": "Lorazépam", "description": "Anxiolytique de la famille des benzodiazépines"},
        {"libelle": "Warfarine", "description": "Anticoagulant oral"},
        {"libelle": "Simvastatine", "description": "Hypolipidémiant, statine"},
        {"libelle": "Ramipril", "description": "Inhibiteur de l'enzyme de conversion, antihypertenseur"},
        {"libelle": "Bisoprolol", "description": "Bêta-bloquant, antihypertenseur"},
        {"libelle": "Diclofénac", "description": "Anti-inflammatoire non stéroïdien"},
        {"libelle": "Fluoxétine", "description": "Antidépresseur, inhibiteur sélectif de la recapture de la sérotonine"},
        {"libelle": "Ciprofloxacine", "description": "Antibiotique de la famille des fluoroquinolones"},
        {"libelle": "Furosémide", "description": "Diurétique de l'anse"},
        {"libelle": "Insuline", "description": "Hormone pancréatique pour le traitement du diabète"},
        {"libelle": "Ventoline", "description": "Bronchodilatateur pour l'asthme"},
        {"libelle": "Prednisolone", "description": "Corticostéroïde, anti-inflammatoire"},
        {"libelle": "Morphine", "description": "Analgésique opioïde puissant"},
        {"libelle": "Ceftriaxone", "description": "Antibiotique de la famille des céphalosporines"},
        {"libelle": "Azithromycine", "description": "Antibiotique de la famille des macrolides"},
        {"libelle": "Allopurinol", "description": "Anti-hyperuricémiant, traitement de la goutte"},
        {"libelle": "Methotrexate", "description": "Immunosuppresseur, cytotoxique"},
        {"libelle": "Aspirine", "description": "Analgésique, anti-inflammatoire, antipyrétique, antithrombotique"},
        {"libelle": "Aténolol", "description": "Bêta-bloquant, antihypertenseur"},
        {"libelle": "Lisinopril", "description": "Inhibiteur de l'enzyme de conversion, antihypertenseur"},
        {"libelle": "Sertraline", "description": "Antidépresseur, inhibiteur sélectif de la recapture de la sérotonine"},
        {"libelle": "Atorvastatine", "description": "Hypolipidémiant, statine"},
    ]
    
    created_medicaments = []
    for med_data in medicaments:
        medicament, created = Medicament.objects.get_or_create(
            libelle_medicament=med_data["libelle"],
            defaults={"description": med_data["description"]}
        )
        created_medicaments.append(medicament)
        if created:
            print(f"Médicament créé: {medicament.libelle_medicament}")
        else:
            print(f"Médicament existant: {medicament.libelle_medicament}")
    
    return created_medicaments

# Création des personnes
def create_personnes(count=50):
    created_personnes = []
    for _ in range(count):
        # Déterminer si c'est un homme ou une femme
        is_male = random.choice([True, False])
        
        civilite = "M." if is_male else random.choice(["Mme", "Mlle"])
        nom = fake.last_name()
        prenom = fake.first_name_male() if is_male else fake.first_name_female()
        
        date_naissance = fake.date_of_birth(minimum_age=18, maximum_age=80)
        
        # Générer un code unique
        code = f"PERS{uuid.uuid4().hex[:8].upper()}"
        
        personne = Personne.objects.create(
            code=code,
            civilite=civilite,
            nom=nom,
            prenom=prenom,
            date_naissance=date_naissance
        )
        created_personnes.append(personne)
        print(f"Personne créée: {personne.civilite} {personne.nom} {personne.prenom}")
    
    return created_personnes

# Création des patients
def create_patients(personnes, count=30):
    created_patients = []
    
    for i in range(min(count, len(personnes))):
        personne = personnes[i]
        
        patient = Patient.objects.create(
            personne=personne
        )
        created_patients.append(patient)
        print(f"Patient créé: {patient.personne.civilite} {patient.personne.nom} {patient.personne.prenom}")
    
    return created_patients

# Création des médecins
def create_medecins(personnes, specialites, count=20):
    titres = ["Dr.", "Prof."]
    created_medecins = []
    
    # Utiliser les personnes qui ne sont pas déjà des patients
    personnes_used = list(Patient.objects.values_list('personne_id', flat=True))
    available_personnes = [p for p in personnes if p.id not in personnes_used]
    
    for i in range(min(count, len(available_personnes))):
        personne = available_personnes[i]
        
        # Générer un code unique pour le médecin
        code_medecin = f"MED{uuid.uuid4().hex[:8].upper()}"
        
        # Créer un médecin (vérifier si code_medecin est un champ du modèle)
        try:
            medecin = Medecin.objects.create(
                personne=personne,
                code_medecin=code_medecin,
                titre_medecin=random.choice(titres)
            )
        except Exception as e:
            # Si code_medecin n'est pas dans le modèle, créer sans ce champ
            if 'code_medecin' in str(e):
                medecin = Medecin.objects.create(
                    personne=personne,
                    titre_medecin=random.choice(titres)
                )
            else:
                raise e
        
        # Affecter des spécialités au médecin (1 à 3 spécialités)
        nb_specialites = random.randint(1, 3)
        selected_specialites = random.sample(list(specialites), nb_specialites)
        
        for specialite in selected_specialites:
            AffecterSpecialite.objects.create(
                medecin=medecin,
                specialite=specialite,
                date_affectation=fake.date_between(start_date='-10y', end_date='today'),
                actif=True
            )
        
        created_medecins.append(medecin)
        print(f"Médecin créé: {medecin.titre_medecin} {medecin.personne.nom} {medecin.personne.prenom} - Spécialités: {[s.libelle for s in selected_specialites]}")
    
    return created_medecins

# Création des consultations
def create_consultations(patients, medecins, admin_user, count=50):
    created_consultations = []
    
    for _ in range(count):
        patient = random.choice(patients)
        medecin = random.choice(medecins)
        
        # Date de consultation dans les 6 derniers mois
        date_consultation = fake.date_time_between(start_date='-6M', end_date='now')
        
        # Date de fin de validité (1 an après la consultation)
        date_fin_validite = date_consultation + timedelta(days=365)
        
        # Générer un code unique pour la consultation
        code_consultation = f"CONS{uuid.uuid4().hex[:8].upper()}"
        
        consultation = Consultation.objects.create(
            code_consultation=code_consultation,
            patient=patient,
            medecin=medecin,
            date_consultation=date_consultation,
            date_fin_validite_consultation=date_fin_validite,
            utilisateur=admin_user
        )
        
        created_consultations.append(consultation)
        print(f"Consultation créée: {consultation.code_consultation} - Patient: {patient.personne.nom} - Médecin: {medecin.personne.nom}")
    
    return created_consultations

# Fonction principale pour exécuter le seeding
def run_seeding():
    print("=== Début du seeding de la base de données ===")
    
    # Demander confirmation avant de supprimer les données existantes
    confirm = input("Attention: Cette opération va supprimer les données existantes. Continuer? (o/n): ")
    if confirm.lower() != 'o':
        print("Opération annulée.")
        return
    
    # Supprimer les données existantes
    clear_data()
    
    # Créer l'utilisateur administrateur
    admin_user = create_admin_user()
    
    # Créer les spécialités
    specialites = create_specialites()
    
    # Créer les types d'actes médicaux
    types_actes = create_types_actes(specialites)
    
    # Créer les médicaments
    medicaments = create_medicaments()
    
    # Créer les personnes
    personnes = create_personnes(count=70)
    
    # Créer les patients
    patients = create_patients(personnes, count=45)
    
    # Créer les médecins
    medecins = create_medecins(personnes, specialites, count=25)
    
    # Créer les consultations
    consultations = create_consultations(patients, medecins, admin_user, count=100)
    
    print("\n=== Récapitulatif ===")
    print(f"- {len(specialites)} spécialités créées")
    print(f"- {len(types_actes)} types d'actes créés")
    print(f"- {len(medicaments)} médicaments créés")
    print(f"- {len(personnes)} personnes créées")
    print(f"- {len(patients)} patients créés")
    print(f"- {len(medecins)} médecins créés")
    print(f"- {len(consultations)} consultations créées")
    
    print("\n=== Seeding terminé avec succès ===")

if __name__ == "__main__":
    run_seeding() 