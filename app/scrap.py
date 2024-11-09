import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .database import init_db_connection, create_table_annonces, insert_annonce


def fetch_annonces(base_url):
    # Connexion à la base de données
    connection = init_db_connection()
    if connection:
        create_table_annonces(connection)  # Création de la table
        page_number = 1
        while True:
            url = f"{base_url}?page={page_number}"
            print(f"Scraping page {page_number} : {url}")

            response = requests.get(url)
            if response.status_code != 200:
                print("Erreur lors de la récupération de la page")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            annonces = soup.find_all('div', class_='card card-list')

            if not annonces:
                print("Aucune annonce trouvée sur cette page, arrêt du scraping.")
                break

            for annonce in annonces:
                try:
                    titre = annonce.find('h3', class_='card-title').get_text(strip=True).replace("à louer", "").strip()
                    date_publi_elements = annonce.find_all('span')
                    date_publi = None
                    for element in date_publi_elements:
                        if 'Publié' in element.get_text():
                            date_publi_text = element.get_text(strip=True)
                            if 'aujourd\'hui' in date_publi_text:
                                date_publi = datetime.now()
                            elif 'hier' in date_publi_text:
                                date_publi = datetime.now() - timedelta(days=1)
                            else:
                                nb_jours = int(date_publi_text.split(' ')[-2])
                                date_publi = datetime.now() - timedelta(days=nb_jours)
                            break

                    prix_et_localisation = annonce.find('h2').get_text(strip=True)
                    prix = int(prix_et_localisation.split('|')[0].strip().replace(' ', '').replace('F', ''))
                    localisation_info = prix_et_localisation.split('|')[1].strip().split(',')
                    quartier = localisation_info[0].strip()
                    ville = localisation_info[1].strip() if len(localisation_info) > 1 else "Ville non spécifiée"

                    meuble = 1 if 'Meublé' in prix_et_localisation else 0
                    nb_chambres_text = titre.split(' ')[1]
                    nb_chambres = int(nb_chambres_text) if nb_chambres_text.isdigit() else None
                    salle_de_bain_texte = annonce.find('h6', class_='card-subtitle mt-1 mb-0 text-muted').get_text(
                        strip=True)
                    nb_salles_de_bain = int(salle_de_bain_texte.split()[0])
                    presence_parking = 1 if 'parking' in salle_de_bain_texte else 0
                    presence_barriere = 1 if 'barrière' in salle_de_bain_texte else 0
                    url_annonce = annonce.find('img', class_='card-img-top lazyload')['data-src']
                    nb_vues = int(annonce.find('i', class_='mdi-eye-circle-outline').find_next_sibling(
                        string=True).strip().split()[0])

                    values = (titre, prix, quartier, ville, nb_chambres, nb_salles_de_bain, url_annonce, nb_vues,
                              presence_parking, presence_barriere, meuble, date_publi)
                    insert_annonce(connection, values)  # Insertion de l'annonce dans la BD
                except Exception as e:
                    print(f"Erreur lors de l'insertion de l'annonce : {e}")

            page_number += 1

        connection.close()  # Fermeture de la connexion
