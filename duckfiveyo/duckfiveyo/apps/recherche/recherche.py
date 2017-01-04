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


KEYWORD = ["album", "cover", "partition"]
REMOVECHAR = [",","+",]
NB_RESULT_BY_QUERY = 5

# Pour utiliser tu fait 
# routineQuery(cequetuveuxchercher)
def createUrl(parametres):
    #genere l'url de google api en fonction des paramètre
    keyApi= 'AIzaSyCxXP6CGk0B1pqIje-VjTjYX44X9XrnoYA' #'AIzaSyDG6Nig_usu4seBML0F2Gn9eC58KeRSIW4'
    Cx = '011588310783855289769:6ld0iqjum24'
    Url = "https://www.googleapis.com/customsearch/v1?key=" + keyApi + "&cx=011588310783855289769:6ld0iqjum24&q="
    newListParam = parametres.split(' ')
    for item in newListParam :
        Url = Url + item + "+"
    Url = Url[:-1]
    return Url
    

def clean_query(query):
    for char in REMOVECHAR:
        query = query.replace(char, "")
    return query

def clean_dico(dico):
    dico_clean = {}
    for query, result in dico.items():
        i = 0
        max = NB_RESULT_BY_QUERY
        for url, value in result.items():
            if i > max:
                break
            if url in dico_clean.keys():
                max += 1
            else:
                dico_clean[url] = value
            i += 1
    return dico_clean

def enrichit_query(query):
    for keyword in KEYWORD:
        if keyword in query:
            query = query.replace(keyword, "")
            while query[-1] == " ":
                query = query[:-1]
    for keyword in KEYWORD:
        yield query + " " + keyword

def get_result_google(query):
    query = clean_query(query)
    dico = {}
    for custom_query in enrichit_query(query):
        url = createUrl(custom_query)
        response = requests.get(url)
        if response.status_code == 200:
            content = json.loads(response.content.decode("utf-8"))
            dico[custom_query] = {}
            for items in content["items"]:
                result_url = items["link"]
                dico[custom_query][result_url] = {}
                dico[custom_query][result_url]["url"] = items.get("link", None)
                dico[custom_query][result_url]["snippet"] = items.get("snippet", None)
                dico[custom_query][result_url]["title"] = items.get("title", None)
        else:
            raise response
    
    dico_clean = clean_dico(dico)

    return dico_clean
    

def get_result_alchemy(google_dico):
    dico = {}
    AlchemyObject = AlchemyAPI()
    for key, value in google_dico.items():
        for i in range(3):
            try:
                url = value["url"]
                response = AlchemyObject.text('url', url)
                # print(str(response["statusInfo"]))
                words = response["text"].split(" ")[:150]
                dico[url] = " ".join(words)
                break
            except KeyError:
                # print(str(i) + "ème echec")
                continue
    return dico


def recupJsonText(Url):
    #Recupere via une url le code Json
    page = requests.get(Url)
    jsonFile= json.loads(page.content.decode("utf-8"))
    return jsonFile
    
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
            
