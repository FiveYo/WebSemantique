try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

# librairie utile pour convertir bytes de l'url en string
import codecs

from urllib.request import urlopen
import json


def getURLsGoogle(query):
    # Clé api google
    locu_api = 'AIzaSyDG6Nig_usu4seBML0F2Gn9eC58KeRSIW4'

    #query = 'piano'

    searchEngine_id = '011588310783855289769:6ld0iqjum24'

    url = 'https://www.googleapis.com/customsearch/v1?q='+query+'&cx='+searchEngine_id+'&key='+locu_api

    reader = codecs.getreader("utf-8")

    json_obj = urlopen(url)

    data = json.load(reader(json_obj))

    print(data.url)
    
    return data.urls


