import sys

import spotlight

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
text = sys.argv[1]
annotations = spotlight.annotate(
    spotlightURL, text, confidence=0.4, support=20, spotter='Default')
print(annotations)
