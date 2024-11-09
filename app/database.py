# database.py
import mysql.connector
from mysql.connector import Error

def init_db_connection():
    """Initialise et renvoie la connexion à la base de données MySQL."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='scrapDB',
            user='root',
            password=''
        )
        if connection.is_connected():
            print("Connexion réussie à MySQL")
            return connection
    except Error as e:
        print("Erreur de connexion MySQL", e)
        return None

def create_table_annonces(connection):
    """Crée la table 'annonces' si elle n'existe pas déjà."""
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS annonces (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titre VARCHAR(255),
                prix INT DEFAULT 0,
                quartier VARCHAR(100),
                ville VARCHAR(100),
                nb_chambres INT,
                nb_salles_de_bain INT,
                url VARCHAR(255),
                nb_vues INT,
                meuble INT, 
                presence_parking TINYINT(1), 
                presence_barriere TINYINT(1), 
                date_publication DATE
            );
        ''')
        print("Table 'annonces' créée ou déjà existante")
    except Error as e:
        print("Erreur lors de la création de la table 'annonces'", e)

def insert_annonce(connection, values):
    """Insère une annonce dans la table 'annonces'."""
    try:
        cursor = connection.cursor()
        query = '''INSERT INTO annonces (titre, prix, quartier, ville, nb_chambres, nb_salles_de_bain, url, nb_vues, presence_parking, presence_barriere, meuble, date_publication)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        cursor.execute(query, values)
        connection.commit()
        print(f"Annonce ajoutée : {values[0]}")
    except Error as e:
        print("Erreur lors de l'insertion de l'annonce : ", e)
