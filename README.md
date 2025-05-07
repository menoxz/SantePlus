# SantePlus - Système de Gestion de Clinique Médicale

SantePlus est une application web complète pour la gestion des activités quotidiennes d'une clinique médicale. Développée avec Django et TailwindCSS, elle offre une interface moderne et intuitive pour la gestion des patients, médecins, consultations, ordonnances et factures.

## 📋 Fonctionnalités

### Gestion des Patients
- Enregistrement des données personnelles et médicales
- Historique complet des consultations et traitements
- Recherche et filtrage avancés

### Gestion des Médecins
- Profils détaillés des médecins et leurs spécialités
- Suivi des disponibilités et plannings
- Attribution des spécialités médicales

### Gestion des Consultations
- Planification et suivi des rendez-vous
- Enregistrement des détails de consultation
- Historique complet accessible aux médecins autorisés

### Gestion des Ordonnances
- Création d'ordonnances numériques
- Association aux consultations et patients
- Génération de PDF pour impression

### Facturation
- Génération automatique de factures
- Suivi des paiements
- Rapports financiers

### Sécurité
- Authentification sécurisée avec verrouillage des comptes
- Gestion des sessions et des droits d'accès
- Protection contre les tentatives d'intrusion

## 🛠️ Technologies Utilisées

- **Backend**: Django 4.2
- **Frontend**: HTML, CSS (TailwindCSS), JavaScript
- **Base de données**: MySQL
- **Sécurité**: Django-Axes pour la protection contre les attaques par force brute
- **Interface**: Design responsive pour accessibilité sur tous les appareils

## 📥 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Virtualenv (recommandé)
- MySQL

### Étapes d'installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/votre-utilisateur/santeplus.git
   cd santeplus
   ```

2. **Créer et activer un environnement virtuel**
   ```bash
   # Sur Windows
   python -m venv venv
   venv\Scripts\activate

   # Sur macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données**
   - Créer une base de données MySQL nommée `santeplus`
   - Configurer les paramètres de connexion dans `santeplus/settings.py`

5. **Appliquer les migrations**
   ```bash
   python manage.py migrate
   ```

6. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

7. **Générer des données de test (optionnel)**
   ```bash
   python seed_data.py
   ```

8. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

9. **Accéder à l'application**
   - Ouvrir un navigateur et accéder à `http://127.0.0.1:8000`
   - Pour l'administration: `http://127.0.0.1:8000/admin`

## 🏗️ Structure du Projet

Le projet est organisé en plusieurs applications Django pour une meilleure modularité:

- **santeplus**: application principale (settings, urls)
- **koumaglo_utilisateurs**: gestion des utilisateurs et authentification
- **koumaglo_patients**: gestion des dossiers patients
- **koumaglo_medecins**: gestion des profils médecins et spécialités
- **koumaglo_consultations**: gestion des rendez-vous et consultations
- **koumaglo_ordonnances**: génération et suivi des ordonnances
- **koumaglo_factures**: facturation et suivi des paiements
- **koumaglo_parametres**: configuration générale du système

## 🖼️ Captures d'écran

*(Des captures d'écran des principales interfaces peuvent être ajoutées ici)*

## 🧪 Tests

Pour exécuter les tests:

```bash
python manage.py test
```

## 📊 Déploiement

### Préparation pour la production

1. Configurer les paramètres de production dans `santeplus/settings.py`
   - Définir `DEBUG = False`
   - Configurer `ALLOWED_HOSTS`
   - Configurer les paramètres de sécurité

2. Collecter les fichiers statiques
   ```bash
   python manage.py collectstatic
   ```

### Options de déploiement

- **Serveur dédié**: Nginx + Gunicorn
- **PaaS**: Heroku, PythonAnywhere, etc.
- **Conteneurs**: Docker avec docker-compose

## 📝 Licence

Ce projet est sous licence [MIT](LICENSE)

## 📞 Contact et Support

Pour toute question ou assistance, veuillez contacter:
- Email: jeanlukou@gmail.com
- Site web: Pas encore disponible

---

Développé avec ❤️ pour améliorer la gestion des soins de santé 