try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

# librairie utile pour convertir bytes de l'url en string
import codecs

from urllib.request import urlopen
import json


def getURLs(query):

    url = 'http://api.duckduckgo.com/?q='+query+'&format=json'

    reader = codecs.getreader("utf-8")

    json_obj = urlopen(url)

    data = json.load(reader(json_obj))
    print(data)

    return data