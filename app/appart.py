import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime, timedelta

def get_total_apartments(connection):
    """Retourne le nombre total d'appartements dans la table 'annonces'."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM annonces")
        total = cursor.fetchone()[0]
        cursor.close()
        return total
    except Error as e:
        print("Erreur lors de la récupération du nombre total d'appartements :", e)
        return 0