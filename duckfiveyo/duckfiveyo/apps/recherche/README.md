# Projet Web Sémantique

## Explications

On va chercher des informations sur des musiques orienté instruments, c'est à dire comme expemple de requêtes:

    !g starway to heaven piano

On va récupérer en premier lieu la musique originale (Youtube, deezer, spotify, etc), ensuite on va chercher les covers associés avec l'instruments
Ensuite, on va chercher les partitions/tablatures/video d'apprentissage. Les informations sur la musique (Wikipédia), instruments présents dans la musique

Nettoyage du code html des pages avec AlchemyAPI, puis identification des entités avec DBpedia Spotlight


## Répartition des tâches

- Requête moteur de recherche + stockage résultats : 
- Résolution d’entit´es dans chacun des textes (DBpedia)
- Construction d'un graphe RDF + relaxation et enrichissement
- Mesure de similarité + graphe
- Visualisation des résultats


## Comment utiliser python

### Première installation :

    $ python -m venv env

Ca va créer l'environnement virtuel.

### Tout le temps

Activation de l'env :

    $ env\Scritps\activate.bat
    $ env\Scripts\activate.ps1 si powershell

On installe les librairies (quand il y en a des nouvelles) :

    (env) $ pip install -r requirements.txt

Si on ajoute une librairie :

    (env) $ pip install *nomDeLaLibrairie*
    (env) $ pip freeze > requirements.txt

Pour sortir de l'env :

    (env) $ desactivate

### Tools

En dehors de l'env installer les outils suivants

- Ipython

### Vocabulaire

**URI** : de l'anglais *Uniform Resource Identifier*, soit littéralement identifiant uniforme de ressource, est une courte chaîne de caractères identifiant une ressource sur un réseau (par exemple une ressource Web) physique ou abstraite, et dont la syntaxe respecte une norme d'Internet mise en place pour le World Wide Web

**API** : interface de programmation applicative, *Application Programming Interface*, est un ensemble normalisé de classes, de méthodes ou de fonctions qui sert de façade par laquelle un logiciel offre des services à d'autres logiciels. Elle est offerte par une bibliothèque logicielle ou un service web, le plus souvent accompagnée d'une description qui spécifie comment des programmes consommateurs peuvent se servir des fonctionnalités du programme fournisseur.

**RDF** : *Resource Description Framework* (RDF) est un modèle de graphe destiné à décrire de façon formelle les ressources Web et leurs métadonnées, de façon à permettre le traitement automatique de telles descriptions.
En annotant des documents non structurés et en servant d'interface pour des applications et des documents structurés (par exemple bases de données et GED) RDF permet une certaine interopérabilité entre des applications échangeant de l'information non formalisée et non structurée sur le Web.

**Triplet RDF** : unité de données la plus petite contenue dans un graphe de type *Resource Description Framework* (RDF) au sein d'une base de données de type triplestore.
Un triplet RDF est une association : ** (sujet, prédicat, objet) **
- **Le sujet** représente la ressource à décrire
- **Le prédicat** représente un type de propriété applicable à cette ressource
- **L'objet** représente une donnée ou une autre ressource : c'est la valeur de la propriété
