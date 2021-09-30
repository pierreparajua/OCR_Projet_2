import time
import requests
from bs4 import BeautifulSoup

start = time.time()
name_category = []


def get_info_1_book(url_book):  # récupère les 10 informations demandées pour 1 livres et retourne une liste
    datas = []
    page = requests.get(url_book)
    if page.ok:
        soup = BeautifulSoup(page.text, features="html.parser")

        universal_product_code = soup.find("td").text
        title = soup.find("h1").text
        price_including_tax = soup.find_all("td")[3].text.strip("Â£")
        price_excluding_tax = soup.find_all("td")[2].text.strip("Â£")
        number_available = [stock for stock in soup.find_all("td")[5].text if stock.isdigit()]
        number_available = ''.join(number_available)
        product_description = soup.find_all("p")[3].text
        category = soup.find_all("a")[3].text
        rating = soup.find_all("div", class_="col-sm-6 product_main")
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

        datas = [url_book, universal_product_code, title, price_including_tax, price_excluding_tax, number_available,
                 product_description, category, review_rating, image_url]
    return datas


def get_books_url(url_category):  # retourne une liste avec l' ensemble des url des livres pour une
    # catégorie donnée
    links = []
    page = requests.get(url_category)
    soup = BeautifulSoup(page.text, features="html.parser")

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


def create_columns():  # permet la création des noms de colonnes
    f.write("product_page_url, universal_ product_code, title, price_including_tax, price_excluding_tax,"
            "number_available, product_description, category, review_rating, image_url\n")


def create_categories_url():  # retourne une liste avec les urls de toutes les catégories de livres (50)
    page = requests.get("https://books.toscrape.com")
    soup = BeautifulSoup(page.text, features="html.parser")
    liste_categories_url = []

    list_category = [i['href'] for i in soup.find_all("a")][3:53]
    for url in list_category:
        full_url = "http://books.toscrape.com/" + url

        liste_categories_url.append(full_url)
    return liste_categories_url


def get_name_category():  # renvoie une liste contenant les noms de catégories
    liste_name = [i.replace("http://books.toscrape.com/catalogue/category/books/", "")[:-13].strip("_") for i in
                  create_categories_url()]
    return liste_name


def get_name_book(url_category):  # extrait les noms des livres par catégorie
    list_book = []
    for url in url_category:

        page = requests.get(url)
        soup = BeautifulSoup(page.text, features="html.parser")
        h3 = [i for i in soup.find_all("h3")]
        for i in h3:
            title = i.find("a")["title"]
            title = title.replace(":", "")
            list_book.append(title)
    return list_book


def get_pictures_url(url_category):
    page = requests.get(url_category)
    soup = BeautifulSoup(page.text, features="html.parser")
    list_url_image = []

    image_url_div = soup.find_all("div", class_="image_container")
    for image_div in image_url_div:
        image_url = "http://books.toscrape.com/" + image_div.find("img")["src"][12:]
        list_url_image.append(image_url)
    return list_url_image


liste_categories = create_categories_url()  # Liste des urls des différentes catégories
list_name_category = get_name_category()  # Liste des noms des catégories
list_name_book = get_name_book(liste_categories)  # Liste de tous les noms de livres

# Enregistrement des fichiers CSV
x = 0
fin = 1000

for url_cat in liste_categories:  # boucle dans la liste de catégorie
    with open(f"data/csv/{list_name_category[x]}.csv", 'a', encoding="utf-8") as f:  # crée un fichier csv par catégorie
        print(f"category: {list_name_category[x]}")
        x += 1
        create_columns()  # Crée les noms de colonne dans le fichier.
        y = 1
        for book in get_books_url(url_cat):  # Boucle sur tous les livres dans chaque catégorie
            print(f"livre {y}")
            print(f"il reste encore {fin} livres ....")
            y += 1
            fin -= 1
            for item in get_info_1_book(book):  # Pour chaque livre extrait et sauve les données sur le fichier .cvs
                f.write(str(item))
                f.write(",")
            f.write("\n")

# Enregistrement des fichiers images
x = 0
for url_cat in liste_categories:  # boucles sur la liste contenant les url des catégories
    list_image = get_pictures_url(url_cat)  # récupère une liste d' url de chaque images par catégorie
    for image in list_image:  # boucle sur cette liste
        image_content = requests.get(image).content  # execute un requête pour chaque url de livre
        with open(f"data/image/{list_name_book[x]}.jpg", "wb") as f:  # sauvegarde l' image dans data/image
            f.write(image_content)
            print(f"image N: {x}")
        x += 1

elapsed = (time.time()) - start
print(f'Temps d\'exécution : {elapsed}s')
