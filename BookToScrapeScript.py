import csv
import regex as re
import requests
from bs4 import BeautifulSoup
import os

urlmain = 'http://books.toscrape.com/index.html'
reponse = requests.get(urlmain)
page = reponse.content
soup = BeautifulSoup(page, "html.parser")

nav = soup.find_all("ul", class_="nav-list")[0].find_all("li")

listegenre = []
listeLivres = []
# Création d'une liste de tous les genre de livres
for i in nav:
    genreLivre = i.find('a').getText()
    listegenre.append(genreLivre.strip().lower())
listegenre = [sp.replace(' ', '-') for sp in listegenre]
listegenre.remove("books")
# Création d'une liste de toutes les urls de chaque categories avec leur pages associées LEN = 80
liste_category_url = []
for numeroPage, genre in enumerate(listegenre):
    current = "current"
    x = f"http://books.toscrape.com/catalogue/category/books/{genre}_{numeroPage + 2}/index.html"
    linkurl = requests.get(x)
    page1 = linkurl.content
    soup1 = BeautifulSoup(page1, "html.parser")
    if current in str(linkurl.content):
        pagecount = soup1.select_one('.current').text.split('of')[-1].strip()
        i = 1
        while i <= int(pagecount):
            x = f"http://books.toscrape.com/catalogue/category/books/{genre}_{numeroPage + 2}/page-{i}.html"
            linkurl = requests.get(x)
            liste_category_url.append(x)
            i = i + 1
    else:
        liste_category_url.append(x)

liste_texturl = liste_category_url

# Création de 2 dossiers
os.mkdir("Images")
os.mkdir("Category")

# Création des titres de chaque page csv
for i in range(len(listegenre)):
    header = ["title", "category", "review_rating", "universal_ product_code (upc)", "price_excluding_tax",
              "price_including_tax", "number_available", "image_url", "product_page_url", "product_description"]
    with open(f"Category/{listegenre[i]}.csv", "w", encoding='UTF8', newline='') as infos_livres:
        writer = csv.DictWriter(infos_livres, fieldnames=header, delimiter=",")
        writer.writeheader()

# Création d'une liste de toutes les urls par categorie LEN = 1000
liste_livre_url = []
for i in range(80):
    urllivre = str(liste_category_url[i])
    rep = requests.get(urllivre)
    page = rep.content
    soup = BeautifulSoup(page, "html.parser")
    pagelivre = soup.select(".product_pod")
    for j in pagelivre:
        b = j.find("a")
        link = b["href"]
        liste_livre_url.append("http://books.toscrape.com/catalogue/" + link)

liste_livre_url = [s.replace('../../../', '') for s in liste_livre_url]

# Création de listes contenants toutes les informations des livres
upcs = []
price_including_tax = []
price_excluding_tax = []
number_available = []
titles = []
category = []
review_rating = []
img_url = []
product_description = []
for a in range(1000):
    urls = str(liste_livre_url[a])
    reponse = requests.get(urls)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")

    # liste titres (on elève certains charactères sinon conflit dans le titre des images)
    titres = soup.find_all("div", class_="col-sm-6 product_main")
    for titre in titres:
        t = titre.find("h1").getText()
        titles.append(t)
    liste_titles = titles
    liste_titles = [v.replace(':', '') for v in liste_titles]
    liste_titles = [r.replace('/', ' ') for r in liste_titles]
    liste_titles = [e.replace('"', '') for e in liste_titles]
    liste_titles = [h.replace('*', 'i') for h in liste_titles]
    liste_titles = [l.replace('?', '') for l in liste_titles]
    # Extraction du nom des catégories
    ctg = soup.find_all("li")
    for i in ctg:
        c = soup.select("a")
        ct = c[3].string
    category.append(ct)
    liste_category = category
    liste_category = [sp.replace(' ', '-') for sp in liste_category]
    # Extraction du rating
    liste_div = []
    stars = ["star-rating One", "star-rating Two", "star-rating Three", "star-rating Four", "star-rating Five"]
    ratings = soup.find("div", class_="content")
    one = stars[0]
    two = stars[1]
    three = stars[2]
    four = stars[3]
    five = stars[4]
    liste_div.append(ratings)
    if stars[0] in str(liste_div):
        review_rating.append("1/5")
    elif stars[1] in str(liste_div):
        review_rating.append("2/5")
    elif stars[2] in str(liste_div):
        review_rating.append("3/5")
    elif stars[3] in str(liste_div):
        review_rating.append("4/5")
    elif stars[4] in str(liste_div):
        review_rating.append("5/5")
    else:
        review_rating.append("0/5")
    liste_review = review_rating

    # Extraction de l'url des images
    images = soup.find("img")
    linkimg = images["src"]
    img_url.append("https://books.toscrape.com/" + linkimg)
    img_url = [t.replace('../../', '') for t in img_url]
    liste_img_url = img_url

    # Extraction des descriptions
    description = soup.find_all("article", class_="product_page")
    p = soup.find_all(["p"])
    prod_desc = p[3].string
    product_description.append(prod_desc)
    liste_product_description = product_description

    # Extractions du numéro upc du prix avec/hors taxes et du nombre d'ouvrages disponibles
    infos = soup.find_all("table", class_="table table-striped")
    td = soup.find_all(["td"])
    upc = td[0].string
    price_ex = td[2].string
    price_in = td[3].string
    number_av = td[5].string
    price_including_tax.append(price_in)
    price_excluding_tax.append(price_ex)
    number_available.append(number_av)
    upcs.append(upc)
    liste_info = (str(upcs) + "\n" + str(
        price_excluding_tax) + "\n" + str(price_including_tax) + "\n" + str(
        number_available))

    results = (str(liste_titles) + "\n" + str(liste_category) + "\n" + str(liste_review) + "\n" + str(
        liste_info) + "\n" + str(liste_img_url) + "\n" + str(liste_product_description))
    results = re.sub(r"[\[\]]", "", str(results))
    # Création d'un dict contenant les listes
    informations = {"title": liste_titles[a], "category": liste_category[a], "review_rating": liste_review[a],
                    "universal_ product_code (upc)": upcs[a],
                    "price_excluding_tax": price_excluding_tax[a], "price_including_tax": price_including_tax[a],
                    "number_available": number_available[a], "image_url": liste_img_url[a], "product_page_url": urls,
                    "product_description": liste_product_description[a]}
    # Ecriture dans les fichiers csv
    header = ["title", "category", "review_rating", "universal_ product_code (upc)", "price_excluding_tax",
              "price_including_tax", "number_available", "image_url", "product_page_url", "product_description"]
    with open(f"Category/{liste_category[a]}.csv", "a", encoding='UTF8', newline='') as infos_livres:
        writer = csv.DictWriter(infos_livres, fieldnames=header, delimiter=",")
        writer.writerow(informations)
    # Téléchargement de toutes les images dans un dossier images avec leur titres respectifs
    r = requests.get(img_url[a], allow_redirects=True)
    open(f"Images/{liste_titles[a]}.jpg", 'wb').write(r.content)
