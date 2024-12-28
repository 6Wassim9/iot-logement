import sqlite3
import random
from datetime import datetime, timedelta

def random_date():
    """
    Génère une date aléatoire dans les 30 derniers jours.
    """
    today = datetime.now()  # Date actuelle
    random_days = random.randint(0, 30)  # Nombre de jours aléatoires entre 0 et 30
    return today - timedelta(days=random_days)  # Retourne une date aléatoire

# Ouverture/initialisation de la base de données
conn = sqlite3.connect('logement.db')
conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par leur nom
c = conn.cursor()

# Fonction pour insérer des capteurs
def inserer_capteurs():
    """
    Insère plusieurs capteurs dans la base de données en fonction des types définis.
    """
    try:
        print("\nInsertion des capteurs dans la table 'Capteur'...")
        
        # Définition des capteurs avec leurs caractéristiques
        capteurs = [
            ('Temp123', 'Cuisine', 1, 1),  # Capteur de température
            ('Hum123', 'Salle de Bain', 2, 7),  # Capteur d'humidité
            ('Lum123', 'Salon', 3, 2),  # Capteur de luminosité
            ('Press123', 'Bureau', 4, 8)  # Capteur de pression atmosphérique
        ]
        
        # Ajout des capteurs dans la table
        for ref_commerciale, ref_piece, IDp, IDt in capteurs:
            c.execute(
                """
                INSERT INTO Capteur (ref_commerciale, ref_piece, IDp, IDt)
                VALUES (?, ?, ?, ?)
                """,
                (ref_commerciale, ref_piece, IDp, IDt)
            )
            print(f"Capteur ajouté : {ref_commerciale} dans {ref_piece} (IDp={IDp}, IDt={IDt})")
        print("Tous les capteurs ont été ajoutés avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des capteurs : {e}")

# Fonction pour insérer des mesures aléatoires
def inserer_mesures():
    """
    Insère des mesures aléatoires pour chaque capteur dans la base de données.
    """
    try:
        print("\nInsertion des mesures dans la table 'Mesure'...")
        c.execute("SELECT IDc, ref_commerciale FROM Capteur")  # Récupérer les capteurs
        capteurs = c.fetchall()

        for capteur in capteurs:
            IDc = capteur['IDc']
            ref_commerciale = capteur['ref_commerciale']

            for _ in range(2):  # Ajouter deux mesures pour chaque capteur
                if "Temp" in ref_commerciale:  # Si capteur de température
                    val = round(random.uniform(-10.0, 50.0), 2)
                elif "Hum" in ref_commerciale:  # Si capteur d'humidité
                    val = round(random.uniform(0.0, 100.0), 2)
                elif "Lum" in ref_commerciale:  # Si capteur de luminosité
                    val = round(random.uniform(100.0, 1000.0), 2)
                elif "Press" in ref_commerciale:  # Si capteur de pression
                    val = round(random.uniform(900.0, 1100.0), 2)
                else:
                    val = round(random.uniform(0.0, 100.0), 2)  # Valeur par défaut

                date_crea = random_date().strftime('%Y-%m-%d %H:%M:%S')  # Date aléatoire
                c.execute(
                    """
                    INSERT INTO Mesure (ref_comerciale, val, date_crea, IDc)
                    VALUES (?, ?, ?, ?)
                    """,
                    (ref_commerciale, val, date_crea, IDc)
                )
                print(f"Mesure ajoutée : Capteur={ref_commerciale}, Valeur={val}, Date={date_crea}")
        print("Toutes les mesures ont été ajoutées avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des mesures : {e}")

# Fonction pour afficher le contenu d'une table
def afficher_table(table_name):
    """
    Affiche tout le contenu de la table spécifiée.
    """
    try:
        print(f"\nContenu de la table '{table_name}' :")
        c.execute(f"SELECT * FROM {table_name}")  # Exécuter une requête SELECT sur la table
        rows = c.fetchall()  # Récupérer toutes les lignes
        for row in rows:
            print(dict(row))  # Afficher chaque ligne sous forme de dictionnaire
    except Exception as e:
        print(f"Erreur lors de l'affichage de la table {table_name} : {e}")

# Exécution des fonctions
try:
    inserer_capteurs()  # Ajouter les capteurs
    inserer_mesures()  # Ajouter les mesures

    # Valider les modifications
    conn.commit()
    print("\nModifications enregistrées avec succès.")

    # Afficher le contenu des tables pour vérification
    afficher_table('Capteur')
    afficher_table('Mesure')

except Exception as e:
    print(f"Erreur lors de l'exécution du script : {e}")
    conn.rollback()  # Annuler les changements en cas d'erreur
finally:
    # Fermeture de la connexion à la base de données
    conn.close()
    print("\nConnexion fermée.")

####################################################################################################
# NB: ce fichier une partie de la reponse sur la question "1.2 Remplissage de la base de données"  #
####################################################################################################