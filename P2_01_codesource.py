import csv
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from slugify import slugify

# Création des chemins des dossiers "data" "csv" et "image"
SOURCE_DIR = Path(__file__).resolve().parent
DATA_DIR = SOURCE_DIR / "data"
CSV_DIR = SOURCE_DIR / "data" / "csv"
IMAGE_DIR = SOURCE_DIR / "data" / "image"


def create_categories_url():  # retourne une liste avec les urls de toutes les catégories de livres (50)
    page = requests.get("https://books.toscrape.com")
    soup = BeautifulSoup(page.content, features="html.parser")
    liste_categories_url = []
    list_category = [i['href'] for i in soup.find_all("a")][3:4]
    for url in list_category:
        full_url = "http://books.toscrape.com/" + url
        liste_categories_url.append(full_url)
    return liste_categories_url


def get_name_category():  # renvoie une liste contenant les noms de catégories
    liste_name = [i.replace("http://books.toscrape.com/catalogue/category/books/", "")[:-13].strip("_") for i in
                  liste_url_categories]
    return liste_name


def get_books_url(url_category):  # retourne une liste avec l' ensemble des urls des livres pour une
    # catégorie donnée
    links = []
    page = requests.get(url_category)
    soup = BeautifulSoup(page.content, features="html.parser")
    # teste le nombre de pages
    if soup.find("li", class_="current") is None:  # s' il y a une seule page
        articles = soup.findAll("article")
        for article in articles:
            a = article.find('a')
            link = a['href'][8:]
            links.append("http://books.toscrape.com/catalogue" + link)
    else:
        nbr_of_pages = soup.find("li", class_="current").text[40:41]  # s' il y a plusieurs pages
        url_category = url_category.replace("index", "page")
        for i in range(1, int(nbr_of_pages) + 1):
            page = requests.get(url_category[:-5] + "-" + str(i) + ".html")
            soup = BeautifulSoup(page.text, features="html.parser")
            articles = soup.findAll("article")
            for article in articles:
                a = article.find('a')
                link = a['href'][8:]
                links.append("http://books.toscrape.com/catalogue" + link)
    return links


def get_info_1_book(url_book):  # récupère les 10 informations demandées pour 1 livres et retourne une liste
    page = requests.get(url_book)
    if page.ok:
        soup = BeautifulSoup(page.content, features="html.parser")
        universal_product_code = soup.find("td").text
        title = soup.find("h1").text
        price_including_tax = soup.find_all("td")[3].text.strip("Â£")
        price_excluding_tax = soup.find_all("td")[2].text.strip("Â£")
        number_available = [stock for stock in soup.find_all("td")[5].text if stock.isdigit()]
        number_available = ''.join(number_available)
        product_description = soup.find_all("p")[3].text
        category = soup.find_all("a")[3].text
        rating = soup.find_all("div", class_="col-sm-6 product_main")  # teste et retourne le nombre d 'étoile
        if "One" in str(rating):
            review_rating = "1"
        elif "Two" in str(rating):
            review_rating = "2"
        elif "Three" in str(rating):
            review_rating = "3"
        elif "Four" in str(rating):
            review_rating = "4"
        else:
            review_rating = "5"
        image_url_div = soup.find("div", {'class': "item active"})
        image_url = "http://books.toscrape.com/" + image_url_div.find("img")["src"][6:]  # recompose l' url des images

        # Crée un dictionnaire pour chaque livre avec les informations demandées
        values = [url_book, universal_product_code, title, price_including_tax, price_excluding_tax, number_available,
                  product_description, category, review_rating, image_url]
        keys = ["product_page_url", "universal_ product_code", "title", "price_including_tax", "price_excluding_tax",
                "number_available", "product_description", "category", "review_rating", "image_url"]
        dict_book = dict(zip(keys, values))

    return dict_book


if DATA_DIR.exists():  # Vérifie l' existence du dossier data
    pass
else:  # Si le dossier n' existe pas, crée le dossier "data" et les sous dossiers "csv" et "image"
    CSV_DIR.mkdir(parents=True)
    IMAGE_DIR.mkdir(parents=True)

liste_url_categories = create_categories_url()  # Liste des urls des différentes catégories
list_name_category = get_name_category()  # Liste des noms des catégories

for url_cat, name_cat in zip(liste_url_categories, list_name_category):  # Itère sur les listes des urls et des noms de
    # catégories
    with open(f"data/csv/{name_cat}.csv", 'w', newline='', encoding="utf-8") as f:  # crée un fichiers csv par catégorie
        headers = ["product_page_url", "universal_ product_code", "title", "price_including_tax", "price_excluding_tax",
                   "number_available", "product_description", "category", "review_rating", "image_url"]
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        print(name_cat)
        for book_url in get_books_url(url_cat):  # Pour chaque livre de cette catégorie, écrie dans une ligne les
            # informations demandées, à partir du dictionnaire crée dans la fonction "get_info_1_book"
            dict_1_book = get_info_1_book(book_url)
            writer.writerow(dict_1_book)
            # Pour chaque livre, récupère et  enregistre l' image du livre dans le dossier "image"
            image_content = requests.get(dict_1_book["image_url"]).content
            slug_name = slugify(dict_1_book["title"])
            with open(f"data/image/{slug_name}.jpg", "wb") as file:  # sauvegarde l' image dans data/image
                file.write(image_content)
            print(slug_name)
