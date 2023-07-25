import requests
from bs4 import BeautifulSoup
import csv
import os

data_title = []
data_books = []

#parcours des pages
for i in range (1,51):
    # URL de la page produit à scraper
    url = f"http://books.toscrape.com/catalogue/page-{i}.html"

    # Obtenir le contenu de la page
    response = requests.get(url)

    # Analyser le contenu avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    #parcours des livres
    for j in range (1,21):
        #stockage des titres et scraping des urls des livres
        title = soup.select_one(f"#default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child({j}) > article > h3 > a")['title']
        url_books = "http://books.toscrape.com/catalogue/" + soup.select_one(f"#default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child({j}) > article > h3 > a")["href"]
        
        
        response = requests.get(url_books)
        soup2 = BeautifulSoup(response.content, 'html.parser')

        #stockage des infos du tableaux
        value = soup2.find_all("td")
        upc = value[0].get_text()
        price_excl_tax = value[2].get_text()
        price_incl_tax = value[3].get_text()
        availability = value[5].get_text()
        review_rating = value[6].get_text()

        #scraping de la catégorie
        category = soup2.select_one("#default > div > div > ul > li:nth-child(3) > a").get_text()

        #scraping de la description des pages et vérification s'il y en a bien une
        if soup2.select_one("#content_inner > article > p"):
            product_desc = soup2.select_one("#content_inner > article > p").get_text()
        else :
            pass


        # Extraction de l'URL de l'image et enregistrement en local
        image_url = "http://books.toscrape.com/" + soup2.select_one("#product_gallery > div > div > div > img")["src"]
        image_response = requests.get(image_url)
        image_filename = image_url.split("/")[-1]
        directory = "book_images"
        if not os.path.exists(directory):
            os.makedirs(directory)
        image_path = os.path.join(directory, image_filename)
        with open(image_path, 'wb') as f:
            f.write(image_response.content)

        # Ajouter les informations à la liste des données
        data_books.append([url_books, upc, title, price_excl_tax, price_incl_tax, availability, review_rating, category, product_desc, image_filename])



# Écrire les données dans un fichier CSV
with open('books.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['product_page_url', 'universal_product_code (upc)', 'title', 'price_excluding_tax', 'price_including_tax', 'number_available', 'review rating', 'category', 'product desc', 'image_url'])
    for book_data in data_books:
        writer.writerow(book_data)
