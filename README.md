# Projet Web Sémantique

## Explications

On va chercher des informations sur des musiques orienté instruments, c'est à dire comme expemple de requêtes:

    !g starway to heaven piano

On va récupérer en premier lieu la musique originale (Youtube, deezer, spotify, etc), ensuite on va chercher les covers associés avec l'instruments
Ensuite, on va chercher les partitions/tablatures/video d'apprentissage. Les informations sur la musique (Wikipédia), instruments présents dans la musique


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

