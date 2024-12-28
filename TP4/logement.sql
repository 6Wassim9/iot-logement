-- Suppression des tables existantes pour éviter les conflits avant la création des nouvelles tables
DROP TABLE IF EXISTS Mesure;
DROP TABLE IF EXISTS Facture;
DROP TABLE IF EXISTS Capteur;
DROP TABLE IF EXISTS Type_Capt;
DROP TABLE IF EXISTS Pieces;
DROP TABLE IF EXISTS Logement;

-- Création de la table Logement : elle contient les informations de base sur chaque logement
CREATE TABLE Logement (
    IDl INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,         -- ID unique de chaque logement, auto-incrémenté
    adresse TEXT,                                           -- Adresse complète du logement
    num_tel TEXT,                                           -- Numéro de téléphone associé au logement
    IP TEXT,                                                -- Adresse IP du serveur lié au logement
    date_crea TIMESTAMP DEFAULT CURRENT_TIMESTAMP           -- Date et heure de création automatique
);

-- Création de la table Pieces : elle représente les pièces associées aux logements
CREATE TABLE Pieces (
    IDp INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,         -- ID unique de chaque pièce, auto-incrémenté
    nom TEXT,                                               -- je l'ai ajouté mais c'est pas nécessaire 
    x INTEGER,                                              -- Coordonnée x de la pièce dans une matrice 3D
    y INTEGER,                                              -- Coordonnée y de la pièce
    z INTEGER,                                              -- Coordonnée z de la pièce
    nbr_capt INTEGER,                                       -- Nombre maximal de capteurs dans la pièce
    IDl INTEGER,                                            -- Référence au logement auquel la pièce appartient
    FOREIGN KEY (IDl) REFERENCES Logement(IDl)              -- Clé étrangère vers Logement(IDl)
);

-- Création de la table Type_Capt : elle définit les types de capteurs ou actionneurs
CREATE TABLE Type_Capt (
    IDt INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,         -- ID unique du type de capteur, auto-incrémenté
    unite TEXT,                                             -- Unité de mesure (ex. °C, %, Lux, etc.)
    precis TEXT                                             -- Précision de mesure (ex. 0.1, 1, etc.)
);

-- Création de la table Capteur : elle contient les informations sur les capteurs ou actionneurs
CREATE TABLE Capteur (
    IDc INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,         -- ID unique du capteur, auto-incrémenté
    ref_commerciale TEXT,                                   -- Référence commerciale unique du capteur
    ref_piece TEXT,                                         -- Description ou référence de la pièce où il se trouve
    date_crea TIMESTAMP DEFAULT CURRENT_TIMESTAMP,          -- Date et heure d'installation du capteur
    IDp INTEGER,                                            -- Référence à la pièce où se trouve le capteur
    IDt INTEGER,                                            -- Référence au type de capteur
    FOREIGN KEY (IDp) REFERENCES Pieces(IDp),               -- Clé étrangère vers Pieces(IDp)
    FOREIGN KEY (IDt) REFERENCES Type_Capt(IDt)             -- Clé étrangère vers Type_Capt(IDt)
);

-- Création de la table Mesure : elle stocke les données collectées par les capteurs
CREATE TABLE Mesure (
    IDm INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,         -- ID unique de la mesure, auto-incrémenté
    ref_comerciale TEXT,                                    -- Référence commerciale liée à la mesure
    val REAL,                                               -- Valeur mesurée
    date_crea TIMESTAMP DEFAULT CURRENT_TIMESTAMP,          -- Date et heure de la mesure
    IDc INTEGER,                                            -- Référence au capteur qui a collecté la mesure
    FOREIGN KEY (IDc) REFERENCES Capteur(IDc)               -- Clé étrangère vers Capteur(IDc)
);

-- Création de la table Facture : elle stocke les factures associées aux logements
CREATE TABLE Facture (
    IDf INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,         -- ID unique de la facture, auto-incrémenté
    type TEXT,                                              -- Type de facture (électricité, eau, etc.)
    date_crea TIMESTAMP DEFAULT CURRENT_TIMESTAMP,          -- Date et heure de création de la facture
    montant REAL,                                           -- Montant de la facture
    val_commerciale REAL,                                   -- Valeur commerciale liée à la facture (ex. consommation)
    IDl INTEGER,                                            -- Référence au logement associé
    FOREIGN KEY (IDl) REFERENCES Logement(IDl)              -- Clé étrangère vers Logement(IDl)
);

-- Insertion d'un logement et de 4 pièces associées
INSERT INTO Logement (adresse, num_tel, IP) 
VALUES ('6 rue Cour des Noues, 75020 Paris', '0123456789', '192.168.1.10');

INSERT INTO Pieces (x, y, z, nbr_capt, IDl) 
VALUES (0, 0, 0, 2, (SELECT IDl FROM Logement ORDER BY date_crea DESC LIMIT 1));
INSERT INTO Pieces (x, y, z, nbr_capt, IDl) 
VALUES (0, 1, 0, 3, (SELECT IDl FROM Logement ORDER BY date_crea DESC LIMIT 1));
INSERT INTO Pieces (x, y, z, nbr_capt, IDl) 
VALUES (1, 0, 0, 1, (SELECT IDl FROM Logement ORDER BY date_crea DESC LIMIT 1));
INSERT INTO Pieces (x, y, z, nbr_capt, IDl) 
VALUES (1, 1, 0, 4, (SELECT IDl FROM Logement ORDER BY date_crea DESC LIMIT 1));

-- Insertion de 8 types de capteurs
INSERT INTO Type_Capt (unite, precis) VALUES ('°C', '0.1');  -- Température
INSERT INTO Type_Capt (unite, precis) VALUES ('Lux', '10');  -- Luminosité
INSERT INTO Type_Capt (unite, precis) VALUES ('W/m²', '5');  -- Solaire
INSERT INTO Type_Capt (unite, precis) VALUES ('kWh', '0.01');-- Consommation électrique
INSERT INTO Type_Capt (unite, precis) VALUES ('cm', '0.5');  -- Niveau d’eau
INSERT INTO Type_Capt (unite, precis) VALUES ('kg', '0.1');  -- Poids
INSERT INTO Type_Capt (unite, precis) VALUES ('%', '1');     -- Humidité
INSERT INTO Type_Capt (unite, precis) VALUES ('hPa', '0.1'); -- Pression atmosphérique

-- Insertion de 4 capteurs/actionneurs
INSERT INTO Capteur (ref_commerciale, ref_piece, IDp, IDt)
VALUES ('Temp123', 'Cuisine', (SELECT IDp FROM Pieces WHERE x=0 AND y=0 AND z=0 LIMIT 1), 
        (SELECT IDt FROM Type_Capt WHERE unite='°C' LIMIT 1));
INSERT INTO Capteur (ref_commerciale, ref_piece, IDp, IDt)
VALUES ('Lum123', 'Salon', (SELECT IDp FROM Pieces WHERE x=0 AND y=1 AND z=0 LIMIT 1), 
        (SELECT IDt FROM Type_Capt WHERE unite='Lux' LIMIT 1));
INSERT INTO Capteur (ref_commerciale, ref_piece, IDp, IDt)
VALUES ('Hum123', 'Salle de Bain', (SELECT IDp FROM Pieces WHERE x=1 AND y=1 AND z=0 LIMIT 1), 
        (SELECT IDt FROM Type_Capt WHERE unite='%' LIMIT 1));
INSERT INTO Capteur (ref_commerciale, ref_piece, IDp, IDt)
VALUES ('Elec123', 'Garage', (SELECT IDp FROM Pieces WHERE x=1 AND y=0 AND z=0 LIMIT 1), 
        (SELECT IDt FROM Type_Capt WHERE unite='kWh' LIMIT 1));

-- Insertion de mesures pour les capteurs
INSERT INTO Mesure (ref_comerciale, val, IDc) 
VALUES ('Temp123', 22.5, (SELECT IDc FROM Capteur WHERE ref_commerciale='Temp123'));
INSERT INTO Mesure (ref_comerciale, val, IDc) 
VALUES ('Temp123', 23.1, (SELECT IDc FROM Capteur WHERE ref_commerciale='Temp123'));
INSERT INTO Mesure (ref_comerciale, val, IDc) 
VALUES ('Lum123', 500.0, (SELECT IDc FROM Capteur WHERE ref_commerciale='Lum123'));
INSERT INTO Mesure (ref_comerciale, val, IDc) 
VALUES ('Lum123', 700.0, (SELECT IDc FROM Capteur WHERE ref_commerciale='Lum123'));

-- Insertion de factures associées au logement
INSERT INTO Facture (type, montant, val_commerciale, IDl) 
VALUES ('Electricité', 100.50, 500, (SELECT IDl FROM Logement ORDER BY date_crea DESC LIMIT 1));
INSERT INTO Facture (type, montant, val_commerciale, IDl) 
VALUES ('Eau', 40.75, 200, (SELECT IDl FROM Logement ORDER BY date_crea DESC LIMIT 1));
INSERT INTO Facture (type, montant, val_commerciale, IDl) 
VALUES ('Déchets', 20.00, 100, (SELECT IDl FROM Logement ORDER BY date_crea DESC LIMIT 1));
INSERT INTO Facture (type, montant, val_commerciale, IDl) 
VALUES ('Internet', 50.00, 150, (SELECT IDl FROM Logement ORDER BY date_crea DESC LIMIT 1));


---------------------------------------------------------------------------------------------------------
-- NB: ce fichier une partie de la reponse sur la question "1.1 Spécifications de la base de données"  --
---------------------------------------------------------------------------------------------------------