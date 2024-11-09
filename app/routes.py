from flask import Blueprint, render_template, request
from flask_paginate import Pagination, get_page_parameter
import pandas as pd

from .database import init_db_connection

main = Blueprint('main', __name__)

def get_apartment_counts(connection):
    """Retourne le nombre total d'appartements, ainsi que ceux de Douala et de Yaoundé."""
    cursor = connection.cursor()
    try:
        # Récupérer le nombre total d'appartements
        cursor.execute("SELECT COUNT(*) FROM annonces")
        total = cursor.fetchone()[0]

        # Récupérer le nombre d'appartements pour Douala
        cursor.execute("SELECT COUNT(*) FROM annonces WHERE ville = 'Douala'")
        douala_count = cursor.fetchone()[0]

        # Récupérer le nombre d'appartements pour Yaoundé
        cursor.execute("SELECT COUNT(*) FROM annonces WHERE ville = 'Yaoundé'")
        yaounde_count = cursor.fetchone()[0]

        # Nombre d'appartements meublés
        cursor.execute("SELECT COUNT(*) FROM annonces WHERE meuble = 1")
        meuble_count = cursor.fetchone()[0]

        return {
            'total': total,
            'douala': douala_count,
            'yaounde': yaounde_count,
            'meuble': meuble_count
        }
    finally:
        cursor.close()



@main.route('/')
def index():
    # Connexion à la base de données
    conn = init_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Requête SQL pour récupérer les 10 appartements les plus vus
    query = """
        SELECT titre, prix, quartier, ville, nb_vues, url
        FROM annonces
        ORDER BY nb_vues DESC
        LIMIT 10
        """
    cursor.execute(query)

    # Récupération des résultats
    appartements = cursor.fetchall()


    # Fermer la connexion
    cursor.close()
    conn.close()

    # Renvoyer les résultats au template
    return render_template('web/index.html', appartements=appartements)

@main.route('/dashboard')
def dashboard():
    # Paramètres pour la pagination
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10  # Nombre d'éléments par page
    offset = (page - 1) * per_page

    # Connexion à la base de données
    conn = init_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Récupérer les données avec la pagination
    query = "SELECT * FROM annonces LIMIT %s OFFSET %s"
    cursor.execute(query, (per_page, offset))
    annonces = cursor.fetchall()

    # 5. Récupérer les noms des colonnes
    column_names = [desc[0] for desc in cursor.description]

    # 6. Convertir les résultats en DataFrame (dataset)
    df = pd.DataFrame(annonces, columns=column_names)

    # Préparer les labels et les données pour le graphique
    indexs = df['nb_chambres'].value_counts().sort_index().index.to_list()
    values = df['nb_chambres'].value_counts().sort_index().to_list()
    labels = [str(index) + "chambre" for index in indexs]

    # Récupérer les 5 appartements les plus populaires
    popular_query = """
       SELECT titre, nb_vues FROM annonces
       ORDER BY nb_vues DESC
       LIMIT 5
       """
    cursor.execute(popular_query)
    popular_apartments = cursor.fetchall()

    # Préparer les données pour le graphique des appartements populaires
    popular_labels = [apt['titre'] for apt in popular_apartments]
    popular_values = [apt['nb_vues'] for apt in popular_apartments]

    # Compter le nombre total d'annonces pour la pagination
    cursor.execute("SELECT COUNT(*) FROM annonces")
    total = cursor.fetchone()['COUNT(*)']

    # Obtenir le nombre total d'appartements
    apartment_counts = get_apartment_counts(conn)

    cursor.close()
    conn.close()

    # Configurer l'objet de pagination
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')

    # Envoyer les données et la pagination au template
    return render_template('dashboard/index.html', annonces=annonces, pagination=pagination, apartment_counts=apartment_counts, labels=labels, values=values,
    popular_labels = popular_labels,
    popular_values = popular_values
    )

@main.route('/list-apartments')
def appartment_list():
    # Paramètres pour la pagination
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10  # Nombre d'éléments par page
    offset = (page - 1) * per_page

    # Connexion à la base de données
    conn = init_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Récupérer les données avec la pagination
    query = "SELECT * FROM annonces LIMIT %s OFFSET %s"
    cursor.execute(query, (per_page, offset))
    annonces = cursor.fetchall()

    # Compter le nombre total d'annonces pour la pagination
    cursor.execute("SELECT COUNT(*) FROM annonces")
    total = cursor.fetchone()['COUNT(*)']

    cursor.close()
    conn.close()

    # Configurer l'objet de pagination
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')

    # Envoyer les données et la pagination au template
    return render_template('dashboard/list-apparts.html', annonces=annonces, pagination=pagination)