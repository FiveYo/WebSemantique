#-*- coding:utf-8 -*-
#
# Utilisation :
# -------------
# import dbspotlight
# data = [(url1, text1), (url2, text2), ...]
# dbspotlight.main(data)
#
# Exemple :
# data = [('url1', 'Mozart'), ('url2', 'Muse')]
# dbspotlight.main(data)
#
# Sortie :
# --------
# {url1: [(triplet RDF 1), (triplet RDF 2), ...],
#  url2: [(triplet RDF 1), (triplet RDF 2), ...],
#  ...
# }
#
# Format d'un triplet
# -------------------
# (sujet, prédicat, objet)
#    -> objet peut être vide (chaine nulle '')
# Exemple : ('Muse', 'type', 'Band')
#           ('Wolfgang_Amadeus_Mozart', 'type', '')

import sys

#import musicbrainzngs
import pprint
import spotlight
import requests

LANG_PORTS = {
    "english": '2222',
    "german": '2226',
    "dutch": '2232',
    "hungarian": '2229',
    "french": '2225',
    "portuguese": '2228',
    "italian": '2230',
    "russian": '2227',
    "turkish": '2235',
    "spanish": '2231'
}

spotlightURL = "http://spotlight.dbpedia.org:{0}/rest/annotate".format(LANG_PORTS[
                                                                       "french"])
spotlightURL = "http://spotlight.dbpedia.org/rest/annotate"
spotlightURL = "http://spotlight.sztaki.hu:{0}/rest/annotate".format(LANG_PORTS[
                                                                     "english"])


def musicbrainz(request):
    musicbrainzngs.set_useragent("duckfiveyo", "v0.1")
    mbz = musicbrainzngs.search_recordings(
        request, limit=1)
    return mbz['recording-list']


def annotations(text):
    try:
        annot = spotlight.annotate(
            spotlightURL, text, confidence=0.4, support=20, spotter='Default')
    except spotlight.SpotlightException:
        annot = ''
    except requests.exceptions.HTTPError:
        annot = ''
    triplets = []
    print(annot)
    for elt in annot:
        subject = elt['URI'][len('http://dbpedia.org/resource/'):]
        function = 'type'
        try:
            objet = elt['types']
        except KeyError:
            objet = ''
        objet = objet.split(',')
        objet = [x[len('DBpedia:'):]
                 for x in objet if x.startswith('DBpedia:')]
        for o in objet:
            triplets.append((subject, function, o))
    return triplets


def main(data):
    output = {}
    for key, value in data.items():
        print(key)
        url = key
        text = value
        output[url] = annotations(text)
    return output

if __name__ == "__main__":
    print("Veuillez importer le fichier comme un module et appeler"
          "la fonction main sur le jeu de données à annoter")