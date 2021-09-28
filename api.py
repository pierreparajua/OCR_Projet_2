import requests
from bs4 import BeautifulSoup

liste_categories_url = []
name_category = []


def get_info_1_book(url_book):  # récupère les 10 informations demandées pour 1 livres et retourne une liste
    page = requests.get(url_book)
    if page.ok:
        soup = BeautifulSoup(page.text, features="html.parser")

        universal_product_code = soup.find("td").text
        title = soup.find("h1").text
        price_including_tax = soup.find_all("td")[3].text.strip("Â£")
        price_excluding_tax = soup.find_all("td")[2].text.strip("Â£")
        number_available = [x for x in soup.find_all("td")[5].text if x.isdigit()]
        number_available = ''.join(number_available)
        product_description = soup.find_all("p")[3].text
        category = soup.find_all("a")[3].text

        # review_rating_p = soup.find("p", {'class': 'star-rating Two'})
        # review_x = review_rating_p.find_all("i", {"class": "icon-star"})

        image_url_div = soup.find("div", {'class': "item active"})
        image_url = "http://books.toscrape.com/" + image_url_div.find("img")["src"][6:]

        datas = [url_book, universal_product_code, title, price_including_tax, price_excluding_tax, number_available,
                 product_description, category, 2, image_url]
    return datas


def get_books_url(url_category):  # retourne une liste avec l' ensemble des url des livres pour une
    # catégorie donnée
    links = []
    page = requests.get(url_category)
    soup = BeautifulSoup(page.text, features="html.parser")

    if soup.find("li", class_="current") is None:  # s' il y a uen seule page
        articles = soup.findAll("article")
        for article in articles:
            a = article.find('a')
            link = a['href'][8:]
            links.append("http://books.toscrape.com/catalogue" + link)
    else:
        nbr_of_pages = soup.find("li", class_="current").text[40:41]  # s' il y a plusieurs pages
        print(nbr_of_pages)
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

    list_category = [i['href'] for i in soup.find_all("a")][3:53]
    for url in list_category:
        x = "http://books.toscrape.com/" + url
        liste_categories_url.append(x)
    return liste_categories_url


def get_name_category():  # renvoie une liste contenant les noms de catégories
    liste_url = create_categories_url()
    liste_name = [i.replace("http://books.toscrape.com/catalogue/category/books/", "")[:-13].strip("_") for i in
                  liste_url]
    return liste_name


stop = len(create_categories_url())
x = 0
fin = 1000
for url_cat in create_categories_url():  # boucle dans la liste de catégorie
    with open(f"data/{get_name_category()[x]}.csv", 'a', encoding="utf-8") as f:  # crée un fichier csv par catégorie
        if x == int(stop):
            break
        print(f"category: {get_name_category()[x]}")
        x += 1
        create_columns()  # Crée les noms de colonne dans le fichier créer
        y = 1
        for book in get_books_url(url_cat):  # Boucle sur tous les livres dans chaques catégories
            print(f"livre {y}")
            print(f"il reste encore {fin} livres ....")
            y += 1
            fin -= 1
            for item in get_info_1_book(book):  # Pour chaque livre extrait et sauve les données sur le fichier .cvs
                f.write(str(item))
                f.write(",")
            f.write("\n")
