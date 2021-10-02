# OCR_projet_2
## Description du projet:
  Ce projet s' incrit dans le cadre de la formation "Developpeur d' application : Python" de OpenClassRooms.
  Le but de ce projet et de créer un programme Python qui récupère différentes informations sur un site de librairie en ligne.
  Ces informations doivent stokées sur des fichiers .csv, et dans un dossier distinc pour les fichiers images.
  
  ## Données scraper par le programme:
   Ce programme récupère les informations du site : https://books.toscrape.com/index.html
   Le programme récupere les données suivantes pour chaque livre :
    -l' URL du livre
    - l' upc ( universal product code)
    - le titre
    - le prix taxe incluse
    - le prix hors taxe
    - le nombre de livre restant en stock
    - la description du livre
    - le catégorie du livre
    - la note du livre
    - l' URL de l 'image
   Ces données sont stokées sur un fichier .csv par catégarie avec les données en titre de colone et chaque ligne correspondant à un livre.
   Le programme crée également un dossier contenant l' ensemble des images des livres du site
   
   ##Pré-requis:
    #Languege de programmation:
      Python3
    #Module utilisés:
      Request
      BeautifulSoup
      Pathlib
      Slugify
    
   

