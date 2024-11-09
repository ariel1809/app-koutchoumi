from flask import Blueprint, render_template, request
from flask_paginate import Pagination, get_page_parameter

from .database import init_db_connection

main = Blueprint('main', __name__)

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

    # Compter le nombre total d'annonces pour la pagination
    cursor.execute("SELECT COUNT(*) FROM annonces")
    total = cursor.fetchone()['COUNT(*)']

    cursor.close()
    conn.close()

    # Configurer l'objet de pagination
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')

    # Envoyer les données et la pagination au template
    return render_template('dashboard/index.html', annonces=annonces, pagination=pagination)

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