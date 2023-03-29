import requests
from bs4 import BeautifulSoup
import csv
import os

# La page d'accueil du site
url = "http://books.toscrape.com/"

# Obtenir le contenu de la page
response = requests.get(url)

# Analyser le contenu avec BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extraire les informations de tous les livres sur toutes les pages
data = []
for page in range(1, 51):
    page_url = f"http://books.toscrape.com/catalogue/page-{page}.html"
    print(page)
    page_response = requests.get(page_url)
    page_soup = BeautifulSoup(page_response.content, 'html.parser')
    books = page_soup.select("article.product_pod")
    for book in books:
        # Extraire l'URL de la page produit
        product_page_url = "http://books.toscrape.com/catalogue/" + book.h3.a["href"]

        # Extraire le code universel de produit (UPC)
        table = book.select("table")
        if table:
            rows = table[0].select("tr")
            upc = rows[0].select("td")[0].get_text()
        else:
            upc = ""
        # Extraire le titre
        title = book.h3.a["title"]

        # Extraire le prix incluant la taxe
        table = book.select("table")
        if table:
            rows = table[0].select("tr")
            price_including_tax = rows[3].select("td")[0].get_text()
        else:
            price_including_tax = ""

        # Extraire le prix excluant la taxe
        if table:
            price_excluding_tax = rows[2].select("td")[0].get_text()
        else:
            price_excluding_tax = ""

        # Extraire le nombre d'exemplaires disponibles
        if table:
            number_available = rows[5].select("td")[0].get_text()
        else:
            number_available = ""

        # Extraire la description du produit
        response = requests.get(product_page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        description = soup.select("article.product_page > p")
        description = description[0].get_text() if description else ""

        # Extraire la catégorie du produit
        category = soup.select("ul.breadcrumb > li")[2].a.get_text()

        # Extraire la note de critique du produit
        review_rating = soup.select("div.product_main > p.star-rating")[0].get("class")[1]

        # Extraire l'URL de l'image et enregistrer localement
        image_url = "http://books.toscrape.com/" + book.select("div.image_container img")[0]["src"]
        image_response = requests.get(image_url)
        image_filename = image_url.split("/")[-1]
        directory = "book_images"
        if not os.path.exists(directory):
            os.makedirs(directory)
        image_path = os.path.join(directory, image_filename)
        with open(image_path, 'wb') as f:
            f.write(image_response.content)

        # Ajouter les informations à la liste des données
        data.append([product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available, description, category, review_rating, image_filename])

# Écrire les données dans un fichier CSV
with open('books.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['product_page_url', 'universal_product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
    for book_data in data:
        writer.writerow(book_data)