import mysql.connector

def get_db_connection():
    """Fonction pour établir une connexion avec la base de données MySQL."""
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='scrapDB'
    )
