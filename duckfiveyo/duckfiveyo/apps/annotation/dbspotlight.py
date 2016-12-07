import sys

import musicbrainzngs
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


def musicbrainzInit():
    musicbrainzngs.set_useragent("duckfiveyo", "v0.1")


def annotations(request, urls, text):
    annot = spotlight.annotate(
        spotlightURL, request, confidence=0.4, support=20, spotter='Default')
    musicbrainzInit()
    mbz = musicbrainzngs.search_recordings(request)
    mbz = [x for x in mbz if x['position'] < 5]
    annot.append(mbz)
    return annot

if __name__ == "__main__":
    text = sys.argv[1]
    print(annotations("", "", text))
