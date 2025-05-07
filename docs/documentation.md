# Documentation de l'Application de Gestion de Clinique

## Introduction

Cette application de gestion de clinique vise à optimiser les tâches quotidiennes des cliniques, en offrant des fonctionnalités pour gérer les patients, les médecins, les consultations, les ordonnances, la facturation et plus encore. Destinée principalement aux secrétaires, elle facilite la gestion administrative tout en assurant un flux de travail efficace.

L'application est développée avec :
- **Framework** : Django, pour sa robustesse et sa prise en charge des bases de données relationnelles.
- **Base de données** : MySQL, pour une gestion efficace des données.
- **Frontend** : HTML avec Tailwind CSS via CDN, pour un design moderne et responsive.
- **Génération de PDF** : ReportLab et WeasyPrint pour l'export de factures et ordonnances.

## Fonctionnalités Principales

Les fonctionnalités sont organisées autour des menus accessibles dans le layout de l'application, chacune correspondant à des tâches spécifiques pour la secrétaire.

### Tableau de Bord de la Secrétaire

Après l'authentification avec un nom d'utilisateur et un mot de passe, la secrétaire est redirigée vers une page de tableau de bord affichant des statistiques clés :
- Nombre de patients enregistrés.
- Nombre de médecins actifs.
- Informations sur les consultations récentes.

Ces statistiques permettent une vue d'ensemble pour une gestion efficace.

### Gestion des Patients

Le menu **Patient** redirige vers une page dédiée avec plusieurs fonctionnalités :
- **Formulaire d'enregistrement** : Permet d'ajouter un nouveau patient si celui-ci n'existe pas dans la base de données, en saisissant des informations comme le nom, prénom, date de naissance, etc.
- **Recherche de patients** : Un formulaire permet de lancer une recherche par nom, facilitant la localisation rapide d'un patient existant. Si le patient n'est pas trouvé, la secrétaire peut utiliser le formulaire d'enregistrement.
- **Liste des patients** : Un tableau affiche la liste des patients, triée du plus récent au plus ancien, avec des colonnes pour le nom, prénom, âge, date de naissance, et une colonne d'actions incluant :
  - Détails du patient.
  - Modification des informations.
  - Ajout d'une consultation pour le patient.
  - Suppression du patient.

### Gestion des Consultations

En cliquant sur le menu **Consultation**, la secrétaire accède à une page avec un formulaire de création de consultation, nécessitant :
- Une date de consultation.
- Une date de fin de validité.
- La sélection d'un patient existant dans la base de données.
- La sélection d'un médecin pour suivre le patient.

Après soumission, elle est redirigée vers la page de détails de la consultation, qui inclut :
- Une liste des ordonnances existantes, le cas échéant.
- Un bouton pour ajouter une nouvelle ordonnance, redirigeant vers un formulaire de création, puis retour à la page de détails après validation.
- Une liste des actes effectués, triée du plus récent au plus ancien, avec possibilité de recherche par type d'acte.
- Un bouton pour ajouter un nouvel acte, redirigeant vers un formulaire où elle sélectionne parmi les types d'actes existants, puis retour à la page de détails.

### Gestion des Ordonnances

Les ordonnances sont gérées dans le contexte des consultations. Chaque ordonnance peut contenir plusieurs détails, chacun spécifiant un médicament et une posologie. La création d'une ordonnance se fait via un formulaire accessible depuis la page de détails de la consultation.

### Gestion de la Facturation

Le module de facturation, récemment implémenté, offre une gestion complète du processus de facturation. Le menu **Facture** donne accès aux fonctionnalités suivantes :

#### Liste des Factures
- Affichage de toutes les factures avec leurs informations essentielles (code, type, patient, date, montant, etc.).
- Indication visuelle du statut de paiement (payée, paiement partiel, non payée).
- Boutons d'action pour chaque facture (détails, modification, suppression).

#### Création de Facture
Le processus de création d'une facture se déroule en plusieurs étapes :
1. **Sélection du patient** : La secrétaire commence par sélectionner un patient dans une liste ou via une recherche.
2. **Sélection de la consultation** : Seules les consultations non facturées du patient sélectionné sont affichées.
3. **Ajout des actes médicaux** : Un formset permet d'ajouter plusieurs actes à facturer, avec les montants récupérés automatiquement via AJAX.
4. **Récapitulatif** : Les montants sont calculés dynamiquement et affichés en temps réel.

#### Détails d'une Facture
La page de détails d'une facture montre :
- Les informations générales de la facture (code, type, date d'émission, etc.).
- Les informations du patient et du médecin concernés.
- La liste des actes facturés avec leur montant.
- L'historique des paiements effectués.
- Un formulaire pour enregistrer un nouveau paiement si la facture n'est pas entièrement payée.
- Un bouton pour imprimer la facture.

#### Gestion des Paiements
- Les paiements peuvent être partiels ou complets.
- La facture est automatiquement marquée comme payée lorsque le montant total est atteint.
- Un historique des paiements est maintenu pour chaque facture.

#### Modification et Suppression
- Une facture peut être modifiée tant qu'elle n'est pas entièrement payée.
- La suppression d'une facture est soumise à une confirmation pour éviter les erreurs.

### Paramètres

Le menu déroulant **Paramètres** offre deux options :
- **Médicaments** : Redirige vers une page avec un formulaire pour ajouter un médicament, incluant diverses informations. Une liste des médicaments existants est disponible, avec des boutons pour voir les détails, modifier ou supprimer, et une fonctionnalité de recherche par nom.
- **Actes Médicaux** : Redirige vers une page avec un formulaire pour ajouter un acte médical, un formulaire de recherche par nom, et une liste de tous les actes avec des actions pour voir les détails, modifier ou supprimer.

### Gestion des Médecins

Le menu **Médecin** mène à une page avec :
- Un formulaire pour ajouter un médecin, nécessitant des informations comme le titre et la sélection d'une spécialité via deux champs de sélection.
- Un formulaire de recherche par nom.
- Une liste de tous les médecins enregistrés, avec des actions pour voir les détails, modifier ou supprimer.

### Gestion du Profil

Le menu **Profil** permet à la secrétaire de consulter et modifier ses informations personnelles, comme le nom, le contact, etc.

### Déconnexion

Un menu **Déconnexion** est disponible pour permettre à la secrétaire de se déconnecter de l'application.

## Modèle de Données

Le modèle de données est basé sur un diagramme de classes détaillé, avec les entités suivantes et leurs attributs, ainsi que leurs relations :

### Entités et Attributs

| **Entité**              | **Attributs**                                                                 |
|-------------------------|------------------------------------------------------------------------------|
| **Utilisateur**         | login, mot_de_passe, actif                                                  |
| **Personne**            | code, nom, prenom, date_naissance, civilite                                |
| **Patient**             | date_enreg (hérite de Personne)                                             |
| **Médecin**             | titre_medecin (hérite de Personne et Utilisateur)                           |
| **Spécialité**          | code, libelle                                                              |
| **AffecterSpécialité**  | date_affectation, actif (liaison pour relation many-to-many avec Médecin)  |
| **TypeActe**            | code, libelle                                                              |
| **Acte**                | code_acte, libelle_acte, montant_acte                                      |
| **Consultation**        | code_consultation, date_consultation, date_fin_validite_consultation       |
| **Ordonnance**          | code_ordonnance, date_ordonnance                                           |
| **OrdonnanceDetail**    | code_ordonnance_detail, posologie_medicament                               |
| **Médicament**          | code_medicament, libelle_medicament                                        |
| **Facture**             | code_facture, type_facture, date_enreg_facture, date_paiement_facture, montant_facture, montant_paye_facture |
| **FactureDetail**       | code_detail_facture, code_acte, montant_facture_detail                     |
| **Paiement**            | id, facture, amount, paymentDate                                           |

### Relations Principales

- Un **Médecin** peut avoir plusieurs **Spécialités** (relation many-to-many via **AffecterSpécialité**).
- Un **Médecin** prescrit plusieurs **Ordonnances** (relation one-to-many).
- Un **Médecin** effectue plusieurs **Consultations** (relation one-to-many).
- Une **Consultation** appartient à un **Patient** et un **Médecin**, enregistrée par un **Utilisateur**, et peut contenir plusieurs **Ordonnances** et **Actes**.
- Une **Facture** appartient à une **Consultation**, peut être établie par un **Médecin** (optionnel), validée par un **Utilisateur**, et composée de plusieurs **Détails de Facture**, chacun référencant un **Acte**.

## Implémentation Technique du Module de Facturation

### Modèles

Le module de facturation s'articule autour de trois modèles principaux :

1. **Facture**
   - Attributs clés : code_facture, type_facture, montant_facture, montant_paye_facture, date_enreg_facture, date_paiement_facture
   - Relations : consultation (ForeignKey), medecin (ForeignKey), utilisateur (ForeignKey)

2. **FactureDetail**
   - Attributs clés : code_detail_facture, montant_facture_detail
   - Relations : facture (ForeignKey), acte (ForeignKey)

3. **Paiement**
   - Attributs clés : amount, paymentDate
   - Relations : facture (ForeignKey)

### Formulaires

Des formulaires spécifiques ont été implémentés pour faciliter la gestion des factures :

1. **FactureForm** : Gère les informations générales de la facture (code, type, consultation liée).
2. **FactureDetailForm** : Gère les détails des actes facturés.
3. **FactureDetailFormSet** : Un formset permettant d'ajouter plusieurs actes à une facture en une seule soumission.
4. **PaiementForm** : Permet d'enregistrer les paiements pour une facture.

### Vues

Les vues principales du module incluent :

1. **facture_list** : Affiche toutes les factures.
2. **facture_detail** : Affiche les détails d'une facture et permet d'ajouter des paiements.
3. **facture_add** / **facture_add_for_patient** : Permet de créer une nouvelle facture.
4. **facture_edit** : Permet de modifier une facture existante.
5. **facture_delete** : Permet de supprimer une facture.
6. **select_patient_for_facture** : Permet de sélectionner un patient avant de créer une facture.
7. **get_acte_montant** : API pour récupérer le montant d'un acte via AJAX.

### Interfaces Utilisateur

Les templates du module de facturation offrent une expérience utilisateur fluide et intuitive :

1. **facture_list.html** : Liste de toutes les factures avec leur statut.
2. **facture_detail.html** : Détails complets d'une facture avec historique des paiements.
3. **facture_form.html** : Formulaire pour créer ou modifier une facture avec un formset pour les actes.
4. **select_patient.html** : Interface pour sélectionner un patient.
5. **facture_confirm_delete.html** : Confirmation avant suppression d'une facture.

### Fonctionnalités JavaScript

Le module utilise JavaScript pour améliorer l'expérience utilisateur :

1. **Calcul dynamique des montants** : Les montants sont calculés en temps réel lors de l'ajout ou de la suppression d'actes.
2. **Récupération AJAX des prix** : Le montant d'un acte est automatiquement récupéré lorsqu'un acte est sélectionné.
3. **Gestion dynamique du formset** : Permet d'ajouter et de supprimer des lignes d'actes de manière interactive.

## Lignes Directrices pour l'Implémentation

- Utiliser l'ORM de Django pour modéliser le schéma de base de données basé sur les entités et relations décrites.
- Mettre en place une authentification et une autorisation pour restreindre l'accès aux fonctionnalités.
- Concevoir une interface utilisateur intuitive, en suivant les principes modernes avec Tailwind CSS.
- Assurer la validation des formulaires pour maintenir l'intégrité des données.
- Implémenter les fonctionnalités de recherche spécifiées, en utilisant les capacités de requête de Django.
- Pour la génération de PDF des factures, envisager des bibliothèques comme **ReportLab** ou **WeasyPrint**.
- Prendre en compte la gestion des dates et heures, notamment pour les consultations et leurs périodes de validité.

## Conclusion

Cette application offre une solution complète pour la gestion des cliniques, couvrant tous les aspects administratifs nécessaires. Elle s'aligne sur les pratiques standard des systèmes de gestion de clinique et peut être enrichie par des projets open-source et des ressources en ligne.

Le module de facturation, désormais pleinement implémenté, offre une gestion efficace des factures et des paiements, complétant ainsi le cycle de gestion administrative de la clinique.

### Gestion des Paramètres

Le module de paramètres permet à l'administrateur de gérer les médicaments et les actes médicaux utilisés dans l'application. Ce module est essentiel pour assurer que les données de l'application sont à jour et pertinentes.

#### Fonctionnalités Principales

- **Gestion des Médicaments** :
  - Ajout de nouveaux médicaments avec des informations telles que le nom, la posologie, et d'autres détails pertinents.
  - Modification et suppression de médicaments existants.
  - Recherche de médicaments par nom.

- **Gestion des Actes Médicaux** :
  - Ajout de nouveaux actes médicaux avec des détails comme le type d'acte et le coût.
  - Modification et suppression d'actes médicaux existants.
  - Recherche d'actes médicaux par nom.

#### Implémentation Technique

##### Modèles

Le module de paramètres s'articule autour de deux modèles principaux :

1. **Médicament**
   - Attributs clés : `code_medicament`, `libelle_medicament`
   - Relations : Aucun

2. **TypeActe**
   - Attributs clés : `code`, `libelle`
   - Relations : Aucun

##### Formulaires

Des formulaires spécifiques ont été créés pour faciliter la gestion des médicaments et des actes médicaux :

1. **MedicamentForm** : Gère les informations des médicaments.
2. **TypeActeForm** : Gère les informations des actes médicaux.

##### Vues

Les vues principales du module incluent :

1. **medicament_list** : Affiche tous les médicaments.
2. **medicament_add** : Permet d'ajouter un nouveau médicament.
3. **medicament_edit** : Permet de modifier un médicament existant.
4. **medicament_delete** : Permet de supprimer un médicament.
5. **type_acte_list** : Affiche tous les actes médicaux.
6. **type_acte_add** : Permet d'ajouter un nouvel acte médical.
7. **type_acte_edit** : Permet de modifier un acte médical existant.
8. **type_acte_delete** : Permet de supprimer un acte médical.

##### Interfaces Utilisateur

Les templates du module de paramètres offrent une expérience utilisateur fluide :

1. **medicament_list.html** : Liste de tous les médicaments avec des options pour modifier ou supprimer.
2. **medicament_form.html** : Formulaire pour ajouter ou modifier un médicament.
3. **type_acte_list.html** : Liste de tous les actes médicaux avec des options pour modifier ou supprimer.
4. **type_acte_form.html** : Formulaire pour ajouter ou modifier un acte médical.

### Conclusion

Le module de paramètres est crucial pour la flexibilité et la mise à jour des données dans l'application. Il permet à l'administrateur de gérer efficacement les médicaments et les actes médicaux, garantissant ainsi que l'application reste pertinente et utile pour les utilisateurs.

## Schéma Complet de la Base de Données

Le schéma de la base de données est conçu pour prendre en charge toutes les fonctionnalités de l'application. Voici une représentation détaillée des tables, de leurs champs et des relations :

### Tables et Champs

| **Table**               | **Champs**                                                                                           | **Clé Primaire**         | **Clés Étrangères**                                      |
|-------------------------|-----------------------------------------------------------------------------------------------------|--------------------------|---------------------------------------------------------|
| **Utilisateur**         | id, login, mot_de_passe, actif                                                                     | id                       | -                                                       |
| **Personne**            | id, code, nom, prenom, date_naissance, civilite                                                   | id                       | -                                                       |
| **Patient**             | id, date_enreg, personne_id                                                                        | id                       | personne_id (Personne)                                  |
| **Médecin**             | id, titre_medecin, personne_id, utilisateur_id                                                    | id                       | personne_id (Personne), utilisateur_id (Utilisateur)    |
| **Spécialité**          | id, code, libelle                                                                                 | id                       | -                                                       |
| **AffecterSpécialité**  | id, medecin_id, specialite_id, date_affectation, actif                                            | id                       | medecin_id (Médecin), specialite_id (Spécialité)        |
| **TypeActe**            | id, code, libelle                                                                                 | id                       | -                                                       |
| **Acte**                | id, code_acte, libelle_acte, montant_acte, type_acte_id                                          | id                       | type_acte_id (TypeActe)                                 |
| **Consultation**        | id, code_consultation, date_consultation, date_fin_validite_consultation, patient_id, medecin_id, utilisateur_id | id                       | patient_id (Patient), medecin_id (Médecin), utilisateur_id (Utilisateur) |
| **Ordonnance**          | id, code_ordonnance, date_ordonnance, consultation_id                                             | id                       | consultation_id (Consultation)                          |
| **OrdonnanceDetail**    | id, code_ordonnance_detail, posologie_medicament, ordonnance_id, medicament_id                   | id                       | ordonnance_id (Ordonnance), medicament_id (Médicament)  |
| **Médicament**          | id, code_medicament, libelle_medicament                                                          | id                       | -                                                       |
| **Facture**             | id, code_facture, type_facture, date_enreg_facture, date_paiement_facture, montant_facture, montant_paye_facture, consultation_id, medecin_id, utilisateur_id | id                       | consultation_id (Consultation), medecin_id (Médecin, optionnel), utilisateur_id (Utilisateur) |
| **FactureDetail**       | id, code_detail_facture, montant_facture_detail, facture_id, acte_id                              | id                       | facture_id (Facture), acte_id (Acte)                    |
| **Paiement**            | id, amount, paymentDate, facture_id                                                              | id                       | facture_id (Facture)                                    |

### Relations

- **Utilisateur** : Un utilisateur peut être lié à un médecin et peut enregistrer des consultations et des factures.
- **Personne** : Base pour les patients et les médecins.
- **Patient** : Lié à une personne, peut avoir plusieurs consultations.
- **Médecin** : Lié à une personne et un utilisateur, peut avoir plusieurs spécialités, consultations, ordonnances et factures.
- **Spécialité** : Peut être attribuée à plusieurs médecins via AffecterSpécialité.
- **AffecterSpécialité** : Table de liaison pour la relation many-to-many entre Médecin et Spécialité.
- **TypeActe** : Catégorie pour les actes médicaux.
- **Acte** : Lié à un type d'acte, peut être inclus dans plusieurs factures via FactureDetail.
- **Consultation** : Liée à un patient, un médecin et un utilisateur, peut avoir plusieurs ordonnances et actes.
- **Ordonnance** : Liée à une consultation, peut avoir plusieurs détails d'ordonnance.
- **OrdonnanceDetail** : Lié à une ordonnance et un médicament.
- **Médicament** : Peut être inclus dans plusieurs détails d'ordonnance.
- **Facture** : Liée à une consultation, un médecin (optionnel) et un utilisateur, peut avoir plusieurs détails de facture et paiements.
- **FactureDetail** : Lié à une facture et un acte.
- **Paiement** : Lié à une facture.

## Structure de Dossier Optionnelle

Voici une structure de dossier recommandée pour organiser le projet Django de l'application de gestion de clinique :

```
projetClinique/
│
├── manage.py              # Script principal pour gérer le projet Django
├── requirements.txt       # Liste des dépendances du projet
├── README.md              # Description générale du projet
│
├── clinique/              # Application principale
│   ├── __init__.py
│   ├── settings.py        # Configuration du projet
│   ├── urls.py            # Routage principal
│   └── wsgi.py            # Point d'entrée WSGI
│
├── apps/                  # Dossier pour les applications Django
│   ├── koumaglo_utilisateurs/      # Gestion des utilisateurs et authentification
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py      # Modèles pour utilisateurs
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── koumaglo_patients/          # Gestion des patients
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py      # Modèles pour patients
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── koumaglo_medecins/          # Gestion des médecins
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py      # Modèles pour médecins et spécialités
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── koumaglo_consultations/     # Gestion des consultations
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py      # Modèles pour consultations
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── koumaglo_ordonnances/       # Gestion des ordonnances
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py      # Modèles pour ordonnances et détails
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── koumaglo_factures/          # Gestion des factures
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   ├── facture_list.html        # Liste des factures
│   │   │   ├── facture_detail.html      # Détails d'une facture
│   │   │   ├── facture_form.html        # Formulaire de création/modification
│   │   │   ├── select_patient.html      # Sélection de patient
│   │   │   └── facture_confirm_delete.html  # Confirmation de suppression
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py      # Modèles pour factures et paiements
│   │   ├── forms.py       # Formulaires spécifiques aux factures
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   └── koumaglo_parametres/        # Gestion des paramètres (médicaments, actes)
│       ├── migrations/
│       ├── templates/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py      # Modèles pour médicaments et actes
│       ├── tests.py
│       ├── urls.py
│       └── views.py
│
├── static/                # Fichiers statiques (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/             # Templates HTML de base
│   ├── base.html          # Template de base avec layout commun
│   ├── dashboard.html     # Tableau de bord
│   └── registration/      # Templates pour authentification
│       ├── login.html
│       └── logout.html
│
├── media/                 # Fichiers uploadés (PDF des factures, etc.)
│
├── docs/                  # Documentation du projet
│   └── documentation.md   # Documentation principale
│
└── tests/                 # Tests globaux du projet
    └── __init__.py
```

### Explication de la Structure

- **clinique/** : Contient les fichiers de configuration principaux du projet Django.
- **apps/** : Divisé en sous-applications pour une meilleure modularité et maintenabilité, chaque application gérant un aspect spécifique (koumaglo_patients, koumaglo_médecins, etc.). Les nome des application doivent êttre précédé de koumaglo_
- **static/** : Contient les fichiers statiques comme les styles CSS personnalisés ou les scripts JS.
- **templates/** : Contient les templates HTML de base, y compris un template `base.html` pour le layout commun avec la barre de navigation.
- **media/** : Pour stocker les fichiers générés comme les PDF des factures.
- **docs/** : Contient la documentation du projet.
- **tests/** : Pour les tests globaux du projet.

Cette structure suit les bonnes pratiques de Django pour un projet modulaire et évolutif, facilitant la maintenance et l'ajout de nouvelles fonctionnalités. 