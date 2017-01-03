from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF
import numpy as np
from difflib import SequenceMatcher

from lxml import html
import requests
import json
import re
import time

import os

if os.environ.get("DJANGO_SETTINGS_MODULE", False):
    from .alchemyapi import *
else:
    from alchemyapi import *

# Pour utiliser tu fait 
# routineQuery(cequetuveuxchercher)
def createUrl(parametres):
    #genere l'url de google api en fonction des paramètre
    keyApi= 'AIzaSyCxXP6CGk0B1pqIje-VjTjYX44X9XrnoYA' #'AIzaSyDG6Nig_usu4seBML0F2Gn9eC58KeRSIW4'
    Cx = '011588310783855289769:6ld0iqjum24'
    Url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyCxXP6CGk0B1pqIje-VjTjYX44X9XrnoYA&cx=011588310783855289769:6ld0iqjum24&q='
    newListParam = parametres.split(' ')
    for item in newListParam :
        Url = Url + item + "+"
    Url = Url[:-1]
    return Url
    
def recupJsonText(Url):
    #Recupere via une url le code Json
    page = requests.get(Url)
    jsonFile= json.loads(page.content.decode("utf-8"))
    return jsonFile

def recupUrlDataVIew (jsonFile):
    #TODO
    #Recupere les donnes clés (artiste ....) 
    
    return 0 
    
def recupUrlText(jsonFile):
    #Recupere l'Url via le code Json
    listeUrl=[]
    listeText = []
    DictItem = jsonFile["items"]
    for itemsIndex in range (len(DictItem)):
        listeUrl.append(DictItem[itemsIndex]["link"])
        listeText.append(DictItem[itemsIndex]["snippet"])
        
    return(listeUrl,listeText)
        

def recupHtmlText(Url):
    #AVec l'url du code Json, on recupere le text du site via Alchemy
    AlchemyObject = AlchemyAPI()
    response = AlchemyObject.text('url', Url)
    text= response["text"]
    if len(text.split(" ")) > 150 :
        text=text[:150]
    return response,text
    
    
def routineQuery(requete):
    
    liste_item_musique  = ["album","cover","partition"]#,"tablature","Unplugged","single","live","Acoustic"]
    st = time.time()
    urlGoogleApiList= []
    urlGoogleApiList.append(createUrl(requete))
    #On regarde si les éléments du dico sont dans la requète
    for item in liste_item_musique:
        if item not in requete:
            urlGoogleApiList.append(createUrl(requete+" "+item))
        else :
            liste_item_musique.remove(item)
            
    dico_query={}
    dico_error={}
    dico_view={}
    listeTemp=liste_item_musique[:]
    listeTemp.append('requete basique')
    #ON range le dictionnaire par nom d'item 
    #on a deux clés la première c'est le nom de la requète : REquète basique ( sans ajout d'item de la liste_item_basique) , Album, cover, partition....
    #la seconde clé c'est L'url qu'on aura trouvé via le parsage du Json 
    #et la value ce sera le text 
    #pour les Url à pb on va les save dans un dico_error et qu'on va refaire tourner plus tard 
    for item in listeTemp:
        for index in range (len(urlGoogleApiList)):
            jsonFile = recupJsonText(urlGoogleApiList[index])
            listTempUrl,listTempText = recupUrlText(jsonFile)
            for indexUrl in range (len(listTempUrl)):
                urlTemp = listTempUrl[indexUrl]
                txtTemp = listTempText[indexUrl]
                
                try : 
                    textTemp = recupHtmlText(urlTemp)[1]
                except KeyError :
                    print("On a ete deco du serv rip")
                    print("Url qui pose problème : ",urlTemp)
                    print("On tente de la relancer ....")
                    try : 
                        textTemp = recupHtmlText(urlTemp)[1]
                    except  KeyError :  
                        print("Nouvelle Erreur WTF ") 
                        textTemp = ""
                        # dico_error[item][urlTemp]="Error"
                    print("Url OK ")
                    
                dico_view[urlTemp]=txtTemp
                dico_query[urlTemp]=textTemp
    print("CA A PRIS : " ,(time.time()-st))
    return dico_query,dico_view
            
        
        
    
            
    
    
    
    
