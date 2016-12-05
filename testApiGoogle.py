try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from urllib.request import urlopen
import json


# Clé api google
locu_api = 'AIzaSyA-pA1EFN5mF5EDZlZZP5H73x3CBRTggHk'

query = 'piano'

searchEngine_id = '015811212802772758694:hxxtt5m5hhk'

url = 'https://www.googleapis.com/customsearch/v1?q='+query+'&cx='+searchEngine_id+'&key='+locu_api

json_obj = urlopen(url)

data = json.load(json_obj)

print(data)


