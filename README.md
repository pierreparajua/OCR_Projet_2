# OCR_projet_2
## Description du projet:
  Ce projet s' incrit dans le cadre de la formation "Développeur d' application : Python" de OpenClassRooms.
  Le but de ce projet et de créer un programme Python qui récupère différentes informations sur un site de librairie en ligne.
  Ces informations doivent être stockées sur des fichiers .csv, et dans un dossier distinct pour les fichiers images.
  
  ## Données scraper par le programme:
   Ce programme récupère les informations sur le  site : https://books.toscrape.com/index.html
   Le programme récupère les données suivantes pour chaque livre :
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
   Ces données sont stockées sur un fichier .csv par catégorie avec les données en titre de colonne et chaque ligne correspondant à un livre.
   Le programme crée également un dossier contenant l' ensemble des images des livres du site
   
   ## Pré-requis:
   - Language de programmation:
      Python3
   - Module utilisés:
      Request
      BeautifulSoup
      Pathlib
      Slugify
    - Un fichier **requirements.txt** est disponible sur le depository
     
   ## Utilisation:
   - Copier le fichier python "codesource" dans le répertoire souhaité
   - Exécuter le programme
   - Le programme crée un dossier "data" dans le repertoire courant, qui contient un dossier "csv" et dossier "image"
   - Les différentes données sont classées dans ces dossiers
  
   ## Version:
   - Ce programme constitue une version bêta qui devra servir à récolter ces informations sur d' autres sites.
    
   ## Auteurs:
   Parajua pierre
   
    
    
   

