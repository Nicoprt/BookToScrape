* Allez dans le terminal et mettez vous dans le dossier désiré via la commande "cd" 
* Pour créer l'environnement virtuel utilisez :
* 'python -m venv' 
* Pour l'activer utilisez soit la commande "source venv/bin/activate" ou "source venv/Scripts/activate" pour Windows
* Une fois l'environnement virtuel créé il faut importer les packages qui sont situés dans le fichier requirements.txt pour cela utilisez la commande:
* "pip install -r requirements.txt" 
* Une fois l'environnement virtuel créé et ayant les bons packages installés entrez la commande "python BookToScrapeScript.py" pour lancer le script.
* Ce script à pour objectif de scrapper la page internet https://books.toscrape.com/index.html et d'en extraires les informations suivantes:
* product_page_url
* universal_ product_code (upc)
* title
* price_including_tax
* price_excluding_tax
* number_available
* product_description
* category
* review_rating
* image_url
* Ces informations sont extraires de tous les livres de la page en plus de télécharger chaque image de chaque livre dans un dossier image.
* Toutes les informations des livres sont extraites et classés par catégories dans leur fichiers .csv respectifs.
