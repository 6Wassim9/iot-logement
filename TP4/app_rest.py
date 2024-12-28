from flask import Flask, jsonify, request, render_template, redirect, url_for
import sqlite3
import requests
from flask_cors import CORS

# Initialisation de l'application Flask
app = Flask(__name__, template_folder='templates')
CORS(app)

# Nom de la base de données SQLite utilisée
DATABASE_NAME = 'logement.db'

# Clé API pour OpenWeatherMap
API_KEY = '28630021b4920d083dd79723622dd4bb'

def get_db_connection():
    """
    Crée une connexion à la base de données SQLite.
    Retourne une connexion avec un row_factory configuré pour récupérer les résultats sous forme de dictionnaires.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """
    Page d'accueil : affiche une introduction et les liens principaux de navigation.
    """
    return render_template('index.html', title='Accueil')

@app.route('/logement')
def logements():
    """
    Route pour afficher tous les logements de la base de données.
    """
    conn = get_db_connection()
    logements = conn.execute('SELECT * FROM Logement').fetchall()
    conn.close()
    return render_template('logement.html', logements=logements, title='Logements')

@app.route('/logement/<int:logement_id>')
def logement(logement_id):
    """
    Page d'un logement spécifique, affichant ses pièces.
    """
    conn = get_db_connection()
    logement = conn.execute('SELECT * FROM Logement WHERE IDl = ?', (logement_id,)).fetchone()
    if not logement:
        conn.close()
        return render_template('error.html', message="Logement introuvable", title="Erreur"), 404

    pieces = conn.execute('SELECT * FROM Pieces WHERE IDl = ?', (logement_id,)).fetchall()
    conn.close()
    return render_template('piece.html', logement=logement, pieces=pieces, title='Pièces')

@app.route('/ajouter_logement', methods=['POST'])
def ajouter_logement():
    try:
        # Récupérer les données du formulaire
        adresse = request.form.get('adresse')
        num_tel = request.form.get('num_tel')
        ip = request.form.get('ip')

        # Vérifier que tous les champs sont fournis
        if not adresse or not num_tel or not ip:
            return jsonify({'error': 'Tous les champs sont obligatoires !'}), 400

        conn = get_db_connection()

        # Vérifier si un logement avec la même adresse ou IP existe déjà
        doublon = conn.execute(
            'SELECT * FROM Logement WHERE adresse = ? OR IP = ?',
            (adresse, ip)
        ).fetchone()

        if doublon:
            conn.close()
            return jsonify({'error': 'Un logement avec cette adresse ou IP existe déjà !'}), 400

        # Insérer le logement dans la base de données
        conn.execute(
            'INSERT INTO Logement (adresse, num_tel, IP) VALUES (?, ?, ?)',
            (adresse, num_tel, ip)
        )
        conn.commit()
        conn.close()

        # Redirection ou réponse JSON de succès
        return jsonify({'message': 'Logement ajouté avec succès !'}), 200

    except KeyError as e:
        return jsonify({'error': f'Champ manquant : {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Erreur interne : {str(e)}'}), 500



@app.route('/check_logement_doublon')
def check_logement_doublon():
    adresse = request.args.get('adresse')
    ip = request.args.get('ip')

    conn = get_db_connection()

    if adresse:
        doublon = conn.execute('SELECT 1 FROM Logement WHERE adresse = ?', (adresse,)).fetchone()
    elif ip:
        doublon = conn.execute('SELECT 1 FROM Logement WHERE IP = ?', (ip,)).fetchone()
    else:
        return jsonify({'error': 'Paramètre manquant'}), 400

    conn.close()
    return jsonify({'exists': bool(doublon)})


@app.route('/modifier_logement', methods=['POST'])
def modifier_logement():
    print(request.form)  # Ajoutez cette ligne pour inspecter les données reçues
    try:
        id = request.form['id']
        adresse = request.form['adresse']
        num_tel = request.form['num_tel']
        ip = request.form['ip']

        conn = get_db_connection()

        # Vérifier si un autre logement avec la même adresse ou IP existe déjà
        doublon = conn.execute('''
            SELECT * FROM Logement
            WHERE (adresse = ? OR IP = ?) AND IDl != ?
        ''', (adresse, ip, id)).fetchone()

        if doublon:
            conn.close()
            return jsonify({'error': 'Un logement avec cette adresse ou IP existe déjà !'}), 400

        # Effectuer la modification
        conn.execute('''
            UPDATE Logement
            SET adresse = ?, num_tel = ?, IP = ?
            WHERE IDl = ?
        ''', (adresse, num_tel, ip, id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Modification réussie"}), 200
    except Exception as e:
        print("Erreur lors de la modification :", e)
        return jsonify({"error": "Erreur lors de la modification du logement"}), 400





@app.route('/supprimer_logement/<int:id>', methods=['POST'])
def supprimer_logement(id):
    """
    Route pour supprimer un logement de la base de données.
    """
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM Logement WHERE IDl = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('logements'))
    except Exception as e:
        return f"Erreur lors de la suppression du logement : {str(e)}", 500

@app.route('/ajouter_piece/<int:logement_id>', methods=['POST'])
def ajouter_piece(logement_id):
    try:
        nom = request.form.get('nom')
        x = request.form.get('x')
        y = request.form.get('y')
        z = request.form.get('z')

        if not nom or not x or not y or not z:
            return jsonify({'error': 'Tous les champs doivent être remplis !'}), 400

        conn = get_db_connection()
        doublon = conn.execute(
            'SELECT * FROM Pieces WHERE nom = ? AND IDl = ?',
            (nom, logement_id)
        ).fetchone()
        if doublon:
            conn.close()
            return jsonify({'error': f'Une pièce avec ce nom existe déjà dans ce logement !'}), 400

        conn.execute(
            '''
            INSERT INTO Pieces (nom, x, y, z, nbr_capt, IDl)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (nom, x, y, z, 0, logement_id)
        )
        conn.commit()
        conn.close()

        return jsonify({'message': 'Pièce ajoutée avec succès !'}), 200

    except Exception as e:
        return jsonify({'error': f'Erreur : {str(e)}'}), 500





@app.route('/modifier_piece', methods=['POST'])
def modifier_piece():
    try:
        # Récupération des données envoyées par le formulaire
        piece_id = request.form.get('id')
        nom = request.form.get('nom')
        x = request.form.get('x')
        y = request.form.get('y')
        z = request.form.get('z')

        # Vérification des champs requis
        if not piece_id or not nom or not x or not y or not z:
            return jsonify({'error': 'Tous les champs doivent être remplis !'}), 400

        conn = get_db_connection()

        # Vérifier si la pièce existe
        logement_id_row = conn.execute('SELECT IDl FROM Pieces WHERE IDp = ?', (piece_id,)).fetchone()
        if not logement_id_row:
            conn.close()
            return jsonify({'error': 'Pièce introuvable !'}), 404

        logement_id = logement_id_row['IDl']

        # Vérification des doublons
        doublon = conn.execute(
            '''
            SELECT 1 FROM Pieces WHERE nom = ? AND IDl = ? AND IDp != ?
            ''',
            (nom, logement_id, piece_id)
        ).fetchone()
        if doublon:
            conn.close()
            return jsonify({'error': 'Une pièce avec ce nom existe déjà dans ce logement !'}), 400

        # Mise à jour de la pièce
        conn.execute(
            '''
            UPDATE Pieces SET nom = ?, x = ?, y = ?, z = ?
            WHERE IDp = ?
            ''',
            (nom, x, y, z, piece_id)
        )
        conn.commit()
        conn.close()

        return jsonify({'message': 'Pièce modifiée avec succès !'}), 200

    except Exception as e:
        # Ajout de détails pour déboguer
        print(f"Erreur dans modifier_piece: {str(e)}")
        return jsonify({'error': 'Erreur interne. Veuillez réessayer plus tard.'}), 500




@app.route('/supprimer_piece/<int:id>', methods=['POST'])
def supprimer_piece(id):
    """
    Route pour supprimer une pièce d'un logement.
    """
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM Pieces WHERE IDp = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(request.referrer)
    except Exception as e:
        return f"Erreur lors de la suppression de la pièce : {str(e)}", 500

@app.route('/factures')
def factures():
    conn = get_db_connection()

    # Récupérer tous les logements
    logements = conn.execute('SELECT * FROM Logement').fetchall()

    conn.close()

    # Renvoyer les données au template
    return render_template('factures.html', logements=[dict(logement) for logement in logements])


@app.route('/factures/<int:logement_id>')
def factures_logement(logement_id):
    conn = get_db_connection()

    # Récupérer les informations du logement
    logement = conn.execute('SELECT * FROM Logement WHERE IDl = ?', (logement_id,)).fetchone()
    if not logement:
        conn.close()
        return "Logement introuvable", 404

    # Récupérer les factures du logement
    factures = conn.execute('''
        SELECT date_crea, type, val_commerciale, montant
        FROM Facture
        WHERE IDl = ?
        ORDER BY date_crea
    ''', (logement_id,)).fetchall()

    # Extraire les données pour le graphique
    factures_dates = [facture['date_crea'].split(' ')[0] for facture in factures]
    factures_valeurs = [facture['val_commerciale'] for facture in factures]

    conn.close()

    return render_template(
        'factures_logement.html',
        logement=logement,
        factures=factures,
        factures_dates=factures_dates,
        factures_valeurs=factures_valeurs
    )


@app.route('/generer_factures/<int:logement_id>', methods=['POST'])
def generer_factures(logement_id):
    try:
        conn = get_db_connection()

        # Vérifier si le logement existe
        logement = conn.execute('SELECT * FROM Logement WHERE IDl = ?', (logement_id,)).fetchone()
        if not logement:
            conn.close()
            return jsonify({"error": "Logement introuvable"}), 404

        # Générer des factures aléatoires
        from datetime import datetime, timedelta
        import random

        types_factures = ['Électricité', 'Eau', 'Gaz']
        for _ in range(10):  # Générer 10 factures
            type_facture = random.choice(types_factures)
            montant = round(random.uniform(50, 500), 2)  # Montant entre 50 et 500 euros
            val_commerciale = round(random.uniform(100, 1000), 2)  # Consommation entre 100 et 1000
            date_crea = datetime.now() - timedelta(days=random.randint(0, 365))  # Date aléatoire dans la dernière année

            conn.execute('''
                INSERT INTO Facture (type, date_crea, montant, val_commerciale, IDl)
                VALUES (?, ?, ?, ?, ?)
            ''', (type_facture, date_crea, montant, val_commerciale, logement_id))

        conn.commit()
        conn.close()
        return jsonify({"message": "Factures générées avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





from datetime import datetime

@app.route('/capteurs/<int:piece_id>')
def capteurs(piece_id):
    conn = get_db_connection()

    # Récupérer les informations de la pièce
    piece = conn.execute('SELECT * FROM Pieces WHERE IDp = ?', (piece_id,)).fetchone()
    if not piece:
        conn.close()
        return "Pièce introuvable", 404

    # Récupérer les capteurs associés à cette pièce
    capteurs = conn.execute('''
        SELECT c.IDc, c.ref_commerciale, c.date_crea, t.unite, t.precis,
               (SELECT val FROM Mesure WHERE IDc = c.IDc ORDER BY date_crea DESC LIMIT 1) AS derniere_valeur,
               (SELECT strftime('%Y-%m-%d %H:%M:%S', date_crea) FROM Mesure WHERE IDc = c.IDc ORDER BY date_crea DESC LIMIT 1) AS heure_mesure
        FROM Capteur c
        JOIN Type_Capt t ON c.IDt = t.IDt
        WHERE c.IDp = ?
    ''', (piece_id,)).fetchall()

    # Mise à jour avec des valeurs aléatoires pour les capteurs
    for capteur in capteurs:
        nouvelle_valeur = None
        if capteur['unite'] == '°C':
            nouvelle_valeur = round(random.uniform(15, 25), 1)  # Température
        elif capteur['unite'] == 'Lux':
            nouvelle_valeur = round(random.uniform(300, 800), 1)  # Luminosité
        elif capteur['unite'] == 'kWh':
            nouvelle_valeur = round(random.uniform(0.5, 5), 2)  # Consommation
        elif capteur['unite'] == 'Pa':
            nouvelle_valeur = round(random.uniform(950, 1050), 1)  # Pression
        elif capteur['unite'] == 'RH':
            nouvelle_valeur = round(random.uniform(30, 70), 1)  # Humidité
        else:
            nouvelle_valeur = round(random.uniform(10, 100), 1)

        heure_actuelle = datetime.now()

        # Mise à jour dans la base de données
        conn.execute(
            'INSERT INTO Mesure (val, IDc, date_crea) VALUES (?, ?, ?)',
            (nouvelle_valeur, capteur['IDc'], heure_actuelle)
        )

    conn.commit()

    # Recharge des capteurs avec les dernières mesures
    capteurs = conn.execute('''
        SELECT c.IDc, c.ref_commerciale, c.date_crea, t.unite, t.precis,
               (SELECT val FROM Mesure WHERE IDc = c.IDc ORDER BY date_crea DESC LIMIT 1) AS derniere_valeur,
               (SELECT strftime('%Y-%m-%d %H:%M:%S', date_crea) FROM Mesure WHERE IDc = c.IDc ORDER BY date_crea DESC LIMIT 1) AS heure_mesure
        FROM Capteur c
        JOIN Type_Capt t ON c.IDt = t.IDt
        WHERE c.IDp = ?
    ''', (piece_id,)).fetchall()

    # Formatter les heures pour le frontend
    formatted_capteurs = []
    for capteur in capteurs:
        heure_mesure = capteur['heure_mesure']
        if heure_mesure:
            formatted_heure = f"le {heure_mesure.split(' ')[0]} à {heure_mesure.split(' ')[1]}"
        else:
            formatted_heure = "N/A"

        formatted_capteurs.append({
            **capteur,
            'heure_mesure': formatted_heure
        })

    # Récupérer les types de capteurs disponibles
    types_capteurs = conn.execute('SELECT * FROM Type_Capt').fetchall()

    # Ajout du logement_id pour la redirection vers l'interface des pièces
    logement_id = piece['IDl']

    conn.close()

    # Ajouter la date actuelle pour limiter les dates futures dans le champ "Date d'installation"
    now = datetime.now().strftime('%Y-%m-%d')

    return render_template(
        'capteurs.html',
        piece=piece,
        capteurs=formatted_capteurs,
        types_capteurs=types_capteurs,
        logement_id=logement_id,
        now=now  # Passer la date actuelle au template
    )


@app.route('/ajouter_capteur/<int:piece_id>', methods=['POST'])
def ajouter_capteur(piece_id):
    try:
        # Récupérer les données du formulaire
        ref_commerciale = request.form.get('ref_commerciale')
        id_type = request.form.get('id_type')
        date_installation = request.form.get('date_installation')

        if not ref_commerciale or not id_type or not date_installation:
            return jsonify({'error': 'Tous les champs doivent être remplis !'}), 400

        # Vérification des doublons
        conn = get_db_connection()
        doublon = conn.execute(
            'SELECT * FROM Capteur WHERE IDp = ? AND ref_commerciale = ?',
            (piece_id, ref_commerciale)
        ).fetchone()

        if doublon:
            conn.close()
            return jsonify({'error': 'Un capteur avec le même nom existe déjà dans cette pièce !'}), 400

        # Insérer le capteur dans la base de données
        conn.execute(
            'INSERT INTO Capteur (ref_commerciale, IDp, IDt, date_crea) VALUES (?, ?, ?, ?)',
            (ref_commerciale, piece_id, id_type, f"{date_installation} 00:00:00")
        )

        # Mettre à jour automatiquement le nombre de capteurs de la pièce
        conn.execute(
            '''
            UPDATE Pieces
            SET nbr_capt = (SELECT COUNT(*) FROM Capteur WHERE IDp = ?)
            WHERE IDp = ?
            ''',
            (piece_id, piece_id)
        )

        conn.commit()
        conn.close()

        return jsonify({'message': 'Capteur ajouté avec succès !'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/modifier_capteur/<int:piece_id>', methods=['POST'])
def modifier_capteur(piece_id):
    try:
        # Récupérer les données du formulaire
        capteur_id = request.form.get('id')
        ref_commerciale = request.form.get('ref_commerciale')
        id_type = request.form.get('id_type')
        date_installation = request.form.get('date_installation')

        if not capteur_id or not ref_commerciale or not id_type or not date_installation:
            return redirect(request.referrer)  # Retourner à la page précédente en cas d'erreur

        # Vérifier si un autre capteur avec le même nom existe dans la même pièce
        conn = get_db_connection()
        doublon = conn.execute(
            '''
            SELECT * FROM Capteur 
            WHERE ref_commerciale = ? 
              AND IDp = ? 
              AND IDc != ?
            ''',
            (ref_commerciale, piece_id, capteur_id)
        ).fetchone()

        if doublon:
            conn.close()
            return redirect(request.referrer)  # Retourner à la page précédente si un doublon est détecté

        # Mettre à jour le capteur dans la base de données
        conn.execute(
            '''
            UPDATE Capteur 
            SET ref_commerciale = ?, IDt = ?, date_crea = ? 
            WHERE IDc = ?
            ''',
            (ref_commerciale, id_type, f"{date_installation} 00:00:00", capteur_id)
        )
        conn.commit()
        conn.close()

        # Redirection vers la page précédente après la modification
        return redirect(request.referrer)

    except Exception as e:
        print(f"Erreur : {e}")
        return redirect(request.referrer)  # Retour à la page précédente en cas d'erreur





@app.route('/supprimer_capteur/<int:id>', methods=['POST'])
def supprimer_capteur(id):
    try:
        conn = get_db_connection()

        # Trouver la pièce associée au capteur
        capteur = conn.execute('SELECT IDp FROM Capteur WHERE IDc = ?', (id,)).fetchone()
        if not capteur:
            conn.close()
            return jsonify({'error': 'Capteur introuvable !'}), 404

        piece_id = capteur['IDp']

        # Supprimer le capteur
        conn.execute('DELETE FROM Capteur WHERE IDc = ?', (id,))

        # Mettre à jour automatiquement le nombre de capteurs dans la pièce
        conn.execute(
            '''
            UPDATE Pieces
            SET nbr_capt = (SELECT COUNT(*) FROM Capteur WHERE IDp = ?)
            WHERE IDp = ?
            ''',
            (piece_id, piece_id)
        )

        conn.commit()
        conn.close()
        return redirect(request.referrer)

    except Exception as e:
        return f"Erreur lors de la suppression du capteur : {str(e)}", 500


@app.route('/check_capteur_doublon/<int:piece_id>')
def check_capteur_doublon(piece_id):
    """
    Vérifie si un capteur avec la même référence commerciale existe déjà dans la pièce.
    """
    ref_commerciale = request.args.get('ref_commerciale')
    if not ref_commerciale:
        return jsonify({'exists': False}), 400

    conn = get_db_connection()
    capteur = conn.execute(
        'SELECT 1 FROM Capteur WHERE IDp = ? AND ref_commerciale = ?',
        (piece_id, ref_commerciale)
    ).fetchone()
    conn.close()

    return jsonify({'exists': bool(capteur)})


import random
from datetime import datetime

@app.route('/update_valeurs/<int:piece_id>', methods=['POST'])
def update_valeurs(piece_id):
    try:
        conn = get_db_connection()

        # Récupérer tous les capteurs de la pièce
        capteurs = conn.execute('SELECT IDc, unite, date_crea FROM Capteur WHERE IDp = ?', (piece_id,)).fetchall()

        updated_capteurs = []  # Liste pour stocker les capteurs mis à jour

        # Générer des valeurs aléatoires et les insérer dans la table Mesure
        for capteur in capteurs:
            date_installation = datetime.strptime(capteur['date_crea'], '%Y-%m-%d %H:%M:%S')
            heure_actuelle = datetime.now()

            # Vérifier que l'heure actuelle est cohérente avec la date d'installation
            if heure_actuelle >= date_installation:
                if capteur['unite'] == '°C':
                    nouvelle_valeur = round(random.uniform(-10, 50), 1)  # Température
                elif capteur['unite'] == 'Lux':
                    nouvelle_valeur = round(random.uniform(0, 1000), 1)  # Luminosité
                elif capteur['unite'] == 'kWh':
                    nouvelle_valeur = round(random.uniform(0, 100), 2)  # Consommation
                else:
                    nouvelle_valeur = round(random.uniform(1, 10), 1)  # Valeur par défaut

                # Insérer la nouvelle valeur dans la base
                conn.execute(
                    '''
                    INSERT INTO Mesure (val, IDc, date_crea)
                    VALUES (?, ?, ?)
                    ''',
                    (nouvelle_valeur, capteur['IDc'], heure_actuelle)
                )

                # Ajouter à la liste des capteurs mis à jour
                updated_capteurs.append({
                    'id': capteur['IDc'],
                    'valeur': nouvelle_valeur,
                    'heure': heure_actuelle.strftime('%Y-%m-%d %H:%M:%S')
                })

        conn.commit()
        conn.close()

        # Retourner les capteurs mis à jour avec leur nouvelle heure
        return jsonify(updated_capteurs), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


from datetime import datetime, timedelta

def remplir_factures_aleatoires():
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('logement.db')
        cursor = conn.cursor()

        # Récupérer les IDs des logements existants
        logements = cursor.execute('SELECT IDl FROM Logement').fetchall()
        if not logements:
            print("Aucun logement trouvé dans la base de données.")
            return
        
        # Définir les types de factures possibles
        types_factures = ['électricité', 'eau', 'gaz', 'chauffage']
        
        # Générer des factures aléatoires
        for logement in logements:
            logement_id = logement[0]
            
            # Générer un nombre aléatoire de factures pour ce logement
            for _ in range(random.randint(5, 15)):  # Entre 5 et 15 factures par logement
                facture_type = random.choice(types_factures)
                montant = round(random.uniform(50, 500), 2)  # Montant aléatoire entre 50€ et 500€
                val_commerciale = round(random.uniform(100, 1000), 1)  # Valeur commerciale entre 100 et 1000
                date_crea = datetime.now() - timedelta(days=random.randint(1, 365))  # Date dans la dernière année
                
                # Insérer la facture dans la base de données
                cursor.execute('''
                    INSERT INTO Facture (type, date_crea, montant, val_commerciale, IDl)
                    VALUES (?, ?, ?, ?, ?)
                ''', (facture_type, date_crea.strftime('%Y-%m-%d %H:%M:%S'), montant, val_commerciale, logement_id))

        # Valider les changements
        conn.commit()
        print("Factures ajoutées avec succès.")
    
    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
    
    except Exception as e:
        print(f"Erreur générale : {e}")
    
    finally:
        if conn:
            conn.close()

# Appeler la fonction
if __name__ == '__main__':
    remplir_factures_aleatoires()


## Partie 2: "2 Serveur RESTful" ##############
############################################################################################

# 2.2 Exercice 2 : serveur web
@app.route('/camembert')
def camembert():
    """
    Génère une page HTML contenant un camembert des données de la table Facture.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT type, SUM(montant) as total FROM Facture GROUP BY type")
        data = cursor.fetchall()

        chart_data = [['Type', 'Montant']]
        for row in data:
            chart_data.append([row['type'], row['total']])

        chart_data_js = str(chart_data)

        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Camembert des Factures</title>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {{'packages':['corechart']}});
                google.charts.setOnLoadCallback(drawChart);
                function drawChart() {{
                    var data = google.visualization.arrayToDataTable({chart_data_js});
                    var options = {{
                        title: 'Répartition des Factures',
                        is3D: true,
                        backgroundColor: '#f5f5f5',
                        legend: {{position: 'bottom'}},
                        fontName: 'Arial',
                        fontSize: 14
                    }};
                    var chart = new google.visualization.PieChart(document.getElementById('piechart'));
                    chart.draw(data, options);
                }}
            </script>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    text-align: center;
                    background-color: #f0f8ff;
                    margin: 0;
                    padding: 0;
                }}
                h1 {{
                    color: #333;
                    margin-top: 20px;
                }}
                #piechart {{
                    margin: 20px auto;
                }}
                nav {{
                    background-color: #333;
                    padding: 10px;
                    text-align: center;
                }}
                nav a {{
                    color: white;
                    text-decoration: none;
                    margin: 0 15px;
                }}
            </style>
        </head>
        <body>
            <nav>
                <a href="/">Accueil</a>
                <a href="/camembert">Camembert</a>
                <a href="/meteo">Météo</a>
            </nav>
            <h1>Répartition des Factures</h1>
            <div id="piechart" style="width: 900px; height: 500px;"></div>
        </body>
        </html>
        """
        return html_template

    except Exception as e:
        return f"Erreur lors de la génération du camembert : {str(e)}"

    finally:
        conn.close()

# 2.3 Exercice 3 : météo
@app.route('/meteo', methods=['GET'])
def meteo():
    """
    Route pour afficher les prévisions météo regroupées par jour pour une ville donnée.
    Si aucune ville n'est spécifiée, utilise 'Paris' par défaut.
    """
    ville = request.args.get('ville', 'Paris')
    base_url = f"http://api.openweathermap.org/data/2.5/forecast?q={ville}&units=metric&lang=fr&appid={API_KEY}"

    try:
        response = requests.get(base_url)
        data = response.json()

        if data['cod'] != "200":
            return f"<h1>Erreur : Ville '{ville}' non trouvée.</h1>"

        daily_forecasts = {}
        for forecast in data['list']:
            date = forecast['dt_txt'].split(' ')[0]
            if date not in daily_forecasts:
                daily_forecasts[date] = {'temp': [], 'descriptions': []}
            daily_forecasts[date]['temp'].append(forecast['main']['temp'])
            daily_forecasts[date]['descriptions'].append(forecast['weather'][0]['description'])

        forecasts = []
        for date, details in list(daily_forecasts.items())[:5]:
            avg_temp = round(sum(details['temp']) / len(details['temp']), 2)
            most_common_desc = max(set(details['descriptions']), key=details['descriptions'].count)
            forecasts.append(f"Date : {date} | Température moyenne : {avg_temp}°C | Description : {most_common_desc}")

        html = f"<h1>Prévisions météo pour {ville} :</h1>"
        html += "<ul>"
        for forecast in forecasts:
            html += f"<li>{forecast}</li>"
        html += "</ul>"

        return html

    except Exception as e:
        return f"<h1>Erreur lors de la récupération des données météo : {str(e)}</h1>"


# 2.4 Exercice 4 : intégration + voir code arduino "sketch_dec16a"
@app.route('/capteur', methods=['POST'])
def recevoir_donnees_capteur():
    """
    Reçoit les données des capteurs (température et humidité) envoyées par l'ESP.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Aucune donnée reçue'}), 400

        temperature = data.get('temperature')
        humidite = data.get('humidite')

        if temperature is None or humidite is None:
            return jsonify({'error': 'Données invalides'}), 400

        conn = get_db_connection()
        if conn:
            conn.execute(
                "INSERT INTO Mesure (val, IDc, date_crea) VALUES (?, ?, datetime('now'))",
                (temperature, 1)
            )
            conn.commit()
            conn.close()

        return jsonify({'message': 'Données reçues et enregistrées avec succès !'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

##########################################Fin de la partie 2#####################################################

#############################################################################################
# NB: tout le reste du code de ce fichier et la partie 3 : "3 HTML/CSS/Javascript"          #
#############################################################################################


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
