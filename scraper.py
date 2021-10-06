import csv
from pathlib import Path
import re

from bs4 import BeautifulSoup
import requests
from slugify import slugify

SOURCE_DIR = Path(__file__).resolve().parent
DATA_DIR = SOURCE_DIR / "data"
CSV_DIR = SOURCE_DIR / "data" / "csv"
IMAGE_DIR = SOURCE_DIR / "data" / "image"

PRODUCTS = ["product_page_url", "universal_ product_code", "title", "price_including_tax", "price_excluding_tax",
            "number_available", "product_description", "category", "review_rating", "image_url", "image_name"]


def do_request(url):
    """
Fonction qui execute un requête sur l' url passer en argument, et utilise BeautifulSoup.
    Args:
        url (str): url pour l requête
    Returns:
        class 'bs4.BeautifulSoup': objet "soup" avec le contenu de la page html
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features="html.parser")
    return soup


def get_category_urls():
    """
Fonction qui récupère l' ensemble des urls de chaque catégorie
    Returns:
        liste: liste des catégories
    """
    soup = do_request("https://books.toscrape.com")
    categories_url = []
    list_category = [i['href'] for i in soup.find_all("a")][3:5]
    for url in list_category:
        full_url = "http://books.toscrape.com/" + url
        categories_url.append(full_url)
    return categories_url


def get_name_categories():
    """
Fonction qui extrait les noms des catégories à partir des urls récupérés dans la fonction "get_category_urls"
    Returns:
        list: des noms de catégorie
    """
    liste_name = [i.replace("http://books.toscrape.com/catalogue/category/books/", "")
                  [:-13].strip("_") for i in get_category_urls()]
    return liste_name


def get_book_urls(url_category):
    """
Fonction qui extrait les urls de chaque livre par catégorie
    Args:
        url_category (str): url de la catégorie souhaitée
    Returns:
        list: des urls de chaque livres

    """
    links = []
    soup = do_request(url_category)
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


def get_info_1_book(url_book):
    """
Fonction qui extrait les informations demandées (PRODUCTS) pour un livre et retourne un dictionnaire
    Args:
        url_book (str): url du livre
    Returns:
        dict: contenant les PRODUCTS en "keys" et les informations en "values"
    """
    soup = do_request(url_book)
    universal_product_code = soup.find("td").text
    title = soup.find("h1").text
    title = re.sub("[(].*?[)]", "", title)  # Supprime le test entre parenthèse dans les titres
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
    image_url = "http://books.toscrape.com/" + image_url_div.find("img")["src"][6:]
    image_name = image_url_div.find("img")["src"][24:]

    # Crée un dictionnaire pour chaque livre avec les informations demandées
    values = [url_book, universal_product_code, title, price_including_tax, price_excluding_tax,
              number_available, product_description, category, review_rating, image_url, image_name]
    keys = PRODUCTS
    dict_book = dict(zip(keys, values))

    return dict_book


def main():
    """
Fonction principale:
    - Crée le dossier "csv" et "image"
    - Sauvegarde les informations dans un fichier csv par catégorie
    - Sauvegarde les images des livres, classés par catégorie
    """
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    for url_cat, name_cat in zip(get_category_urls(), get_name_categories()):
        with open(f"data/csv/{name_cat}.csv", 'w', newline='', encoding="utf-8") as f:
            headers = PRODUCTS
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            print(name_cat)
            liste_dict = []
            (IMAGE_DIR / name_cat).mkdir(parents=True, exist_ok=True)
            for book_url in get_book_urls(url_cat):
                dict_1_book = get_info_1_book(book_url)
                liste_dict.append(dict_1_book)

                image_content = requests.get(dict_1_book["image_url"]).content
                slug_name = slugify(dict_1_book["title"])
                with open(f"data/image/{name_cat}/{slug_name}.jpg", "wb") as file:
                    file.write(image_content)
                print(slug_name)
            writer.writerows(liste_dict)


if __name__ == "__main__":
    main()
