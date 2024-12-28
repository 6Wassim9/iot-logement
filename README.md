# Projet IoT - Logement Éco-Responsable

Ce projet a été développé dans le cadre du TP "Logement Éco-Responsable". Il consiste en une application IoT permettant de gérer des logements, pièces, capteurs, mesures et factures via une interface web et un serveur Flask. Le projet met également en œuvre des graphiques dynamiques et l'intégration d'une API météo.

---

## Contenu de l'archive

### Structure des fichiers
Voici une description des principaux fichiers et répertoires :

```
TP4/
├── app_rest.py            # Serveur Flask RESTful
├── logement.sql           # Script SQL pour créer et initialiser la base de données
├── logement.db            # Base de données SQLite
├── remplissage.py         # Script Python pour insérer des données dans la base
├── static/                # Dossier des fichiers CSS, JS et Bootstrap
│   ├── css/
│   │   └── styles.css     # Feuille de style principale
│   ├── js/
│   │   └── scripts.js     # Scripts dynamiques pour l'interface utilisateur
│   └── vendor/            # Fichiers Bootstrap
├── templates/             # Templates HTML pour l'interface web
│   ├── base.html          # Modèle de base pour les autres pages
│   ├── index.html         # Page d'accueil
│   ├── logement.html      # Liste des logements
│   ├── piece.html         # Gestion des pièces
│   ├── capteurs.html      # Gestion des capteurs
│   ├── mesures.html       # Affichage des mesures
│   ├── factures.html      # Liste des factures par logement
│   ├── factures_logement.html # Détails des factures
│   └── error.html         # Page d'erreur
└── README.md              # Documentation du projet
```

---

## Comment faire fonctionner le projet

### Prérequis
Assurez-vous que les dépendances suivantes sont installées sur votre machine :

- Python 3.x
- `pip` (gestionnaire de paquets Python)

### Bibliothèques Python nécessaires
Voici la liste complète des bibliothèques Python utilisées :

1. **Bibliothèques standards (incluses avec Python) :**
   - `sqlite3` : Gestion de la base de données SQLite.
   - `random` : Génération de valeurs aléatoires pour les tests.
   - `datetime` : Gestion des dates et heures.

Ces bibliothèques sont incluses par défaut avec Python, aucune installation supplémentaire n'est requise.

2. **Bibliothèques tierces :**
   - `flask` : Framework pour créer le serveur web.
   - `flask_cors` : Gestion des requêtes CORS pour le serveur.
   - `requests` : Requêtes HTTP pour l'API météo.

### Installation des dépendances tierces
Pour installer les bibliothèques tierces, exécutez les commandes suivantes dans un terminal :

```bash
# Mise à jour de pip (facultatif mais recommandé)
pip install --upgrade pip

# Installation des bibliothèques nécessaires
pip install flask flask-cors requests
```

### Étapes pour lancer l'application

1. **Télécharger l'ensemble du code**
   - Sur GitHub ou GitLab de l'université télécharger le dossier TP4.zip et mettez le dans un endroit dans votre machine.
   - Dezipper le dossier TP4.zip.
   - NB: il est recommander d'utilisant un environnement de développement intégré spécialiser telque VScode.
     
3. **Initialiser la base de données :**
   - Exécutez le script `logement.sql` pour créer les tables nécessaires.
   - Vous pouvez également utiliser le fichier `remplissage.py` pour insérer des données de test.

4. **Lancer le serveur :**
   - Ouvrez un terminal dans le dossier contenant `app_rest.py`.
   - Exécutez la commande :
     ```bash
     python app_rest.py
     ```
   - Le serveur sera disponible sur `http://localhost:5000`.

5. **Accéder à l'interface utilisateur :**
   - Ouvrez un navigateur et allez à l'adresse `http://localhost:5000`.

6. **API météo :**
   - Le serveur utilise l'API OpenWeatherMap pour récupérer des prévisions météo. Assurez-vous que la clé API est définie dans `app_rest.py`.

---

## Répartition par exercice

### Partie 1 : Base de données
- Le modèle relationnel de la base de données est défini dans `logement.sql`.
- Exemples de requêtes SQL pour créer les tables et insérer des données.
- Remplissage des données initiales via `remplissage.py` (lignes principales commentées).

### Partie 2 : Serveur RESTful
- Serveur Flask implémenté dans `app_rest.py`.
- Routes principales :
  - `/logement` : Liste des logements.
  - `/logement/<id>` : Détails des pièces d'un logement.
  - `/capteurs` : Gestion des capteurs.
  - `/factures` : Gestion des factures.
  - `/meteo` : Prévisions météo.
- Chaque route est documentée dans le code avec des commentaires explicatifs.

### Partie 3 : Interface utilisateur
- Templates HTML dans le dossier `templates/`.
- Styles définis dans `static/css/styles.css`.
- Scripts pour l'interactivité et les graphiques : `static/js/scripts.js`.
- Intégration de Chart.js pour les graphiques interactifs (factures et mesures).

---

## Ressources et aides utilisées

1. **Utilisation de ChatGPT** :
   - ChatGPT a été utilisé pour générer des suggestions de syntaxe et clarifier certains concepts liés à Flask, SQLite et Chart.js.
   - Les portions de code inspirées ou générées à l'aide de ChatGPT sont annotées directement dans les fichiers correspondants avec des commentaires explicites.

---

## Notes importantes
- Toute ressource utilisée, comme ChatGPT, est mentionnée dans le code avec des commentaires explicites.
- Ce projet est personnel et respecte les consignes d'intégrité académique.

---

## Auteurs
- **Wassim GHACHI EI4 TPB1** : Développement complet et intégration des différentes parties.
