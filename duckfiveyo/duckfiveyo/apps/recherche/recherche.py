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
NB_TIRET_TAB = 40
NB_ACCORD_PART = 20
DELIMITER = [" ", "\n", "/", "[", "]", "(", ")"]
ACCORDS = [
    "A", "A#", "Ab", "B", "Bb", "C", "C#", "D", "D#", "Db", "E", "Eb", "F", "F#", "G", "G#", "Gb",
    "Am", "Amin", "A6", "Am6", "A7", "A9",
    "A#m", "A#min", "A#6", "A#m6", "A#7", "A#9",
    "B#m", "B#min", "B#6", "B#m6", "B#7", "B#9",
    "Cm", "Cmin", "C6", "Cm6", "C7", "C9",
    "C#m", "C#min", "C#6", "C#m6", "C#7", "C#9",
    "Dm", "Dmin", "D6", "Dm6", "D7", "D9",
    "D#m", "D#min", "D#6", "D#m6", "D#7", "D#9",
    "Em", "Emin", "E6", "Em6", "E7", "E9",
    "Fm", "Fmin", "F6", "Fm6", "F7", "F9",
    "F#m", "F#min", "F#6", "F#m6", "F#7", "F#9",
    "Gm", "Gmin", "G6", "Gm6", "G7", "G9",
    "G#m", "G#min", "G#6", "G#m6", "G#7", "G#9",
    "Abm", "Abmin", "Ab6", "Abm6", "Ab7", "Ab9",
    "Bbm", "Bbmin", "Bb6", "Bbm6", "Bb7", "Bb9",
    "Cbm", "Cbmin", "Cb6", "Cbm6", "Cb7", "Cb9",
    "Dbm", "Dbmin", "Db6", "Dbm6", "Db7", "Db9",
    "Ebm", "Ebmin", "Eb6", "Ebm6", "Eb7", "Eb9",
    "Fbm", "Fbmin", "Fb6", "Fbm6", "Fb7", "Fb9",
    "Gbm", "Gbmin", "Gb6", "Gbm6", "Gb7", "Gb9",
]



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
                try:
                    dico[custom_query][result_url]["thumbnail"] = items["pagemap"]["cse_thumbnail"][0]["src"]
                    dico[custom_query][result_url]["video"] = items["pagemap"]["videoobject"][0]["embedurl"]
                except KeyError as k:
                    print(k)
        else:
            raise response
    
    dico_clean = clean_dico(dico)

    return dico_clean
    

def get_result_alchemy(google_dico):
    dico = {}
    AlchemyObject = AlchemyAPI()
    dico["mathieu"] = {}
    dico["quentin"] = {}
    for key, value in google_dico.items():
        for i in range(3):
            try:
                url = value["url"]
                response = AlchemyObject.text('url', url)
                # print(str(response["statusInfo"]))
                words = response["text"].split(" ")[:150]

                dico["quentin"][url] = {}
                
                dico["mathieu"][url] = " ".join(words)
                dico["quentin"][url]["url"] = url
                dico["quentin"][url]["text"] = response["text"]
                dico["quentin"][url]["info"] = info_partition(response["text"])
                break
            except KeyError:
                # print(str(i) + "ème echec")
                continue
    return dico


def info_partition(text):
    nb_tiret = text.count("-") + text.count("\u2014")
    is_tab = nb_tiret > NB_TIRET_TAB

    nb_accord = count_accord(text)
    is_part = nb_accord > NB_ACCORD_PART
    # check si c'est une tablature
    # check si il y a des accords
    partition = None
    tab = None

    if is_part:
        partition = extract_part(text)
    if is_tab:
        tab = extract_tab(text)

    return {
        "tab": tab,
        "partition": partition
    }

def count_accord(text):
    result = 0
    delimiter = "|".join(DELIMITER)
    list_word = re.split(delimiter,text)
    for accord in ACCORDS:
        result += list_word.count(accord)
    return result

def extract_part(text):
    start, last = index_chord(text)
    return text[start:last]


def index_chord(text):
    result = []
    for accord in ACCORDS:
        index = text.find(accord)
        if index > 0:
            result.append(index)
    return min(result), max(result)

def extract_tab(text):
    indices_tiret = [i for i, x in enumerate(text) if x == "-" or x == "\u2014"]
    # cherche le premier index qui nous interesse pas le premier tiret
    iterat = iter(indices_tiret)

    print(indices_tiret)

    start = 0
    end = 0

    for index in indices_tiret:
        try:
            if text[index + 1] == "-" or text[index + 1] == "\u2014":
                start = index
                break
        except:
            break
    

    for index in reversed(indices_tiret):
        try:
            if text[index - 1] == "-" or text[index - 1] == "\u2014":
                end = index
                break
        except:
            break
    return text[start:end]

