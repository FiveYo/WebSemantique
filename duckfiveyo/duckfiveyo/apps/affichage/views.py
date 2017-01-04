from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from duckfiveyo.apps.annotation.dbspotlight import main
from duckfiveyo.apps.graphe.graphRDF import graphRDF
from duckfiveyo.apps.mergeSimilarite.graphMerge import routineMatrice

from duckfiveyo.apps.recherche.recherche import get_result_google, get_result_alchemy

from .models import Query, GoogleResult, AlchemyResult

import json
import pprint

def home(request):
    return render_to_response("home.html")


def ask(request):
    if request.method == "POST":
        arguments = request.POST
    elif request.method == "GET":
        arguments = request.GET
    else:
        return HttpResponseNotAllowed(("GET", "POST"))

    query = arguments["query"]

    query_up = query.upper()

    try:
        model_query = Query.objects.get(query=query_up)
        g_result = json.loads(model_query.googleresult.result)
        a_result = json.loads(model_query.alchemyresult.result)
    except ObjectDoesNotExist:
        model_query = Query(query=query_up)
        model_query.save()
        g_result = get_result_google(query_up)
        model_g_result = GoogleResult(
            query=model_query,
            result=json.dumps(g_result)
        )
        model_g_result.save()

        a_result = get_result_alchemy(g_result)
        model_a_result = AlchemyResult(
            query=model_query,
            result=json.dumps(a_result)
        )
        model_a_result.save()
    except MultipleObjectsReturned:
        # remove ceux qui sont vide
        pass

    
    partition = []
    for key, value in a_result["quentin"].items():
        if value["info"]["tab"] or value["info"]["partition"]:
            partition.append(g_result[key])

    # for key, result in a_result["quentin"].items():
    #     pprint.pprint(result)
    # triplet = main(a_result)

    categories = ["album", "cover", "partition", "tablature", "chords"]

    dico = graphRDF(a_result["mathieu"])

    dico_milly = routineMatrice(dico, categories)

    pprint.pprint(dico_milly)

    album_url_list = dico_milly[categories[0]]
    cover_url_list = dico_milly[categories[1]]
    partition_url_list = dico_milly[categories[2]]
    tab_url_list = dico_milly[categories[3]]
    chords_url_list = dico_milly[categories[4]]


    cover = []

    for url in cover_url_list:
        cover.append(g_result[url])
    
    #   print(triplet)

    # dicoMilly = graphRDF(triplet)

    # queryList = [query,query+" cover",query+" partition",query+" album"]

    # resultfinal = routineMatrice(dicoMilly, queryList, 0.5)

    # web = resultfinal[query]
    # cover = resultfinal[query+" cover"]
    # album = resultfinal[query + " album"]
    # partition = resultfinal[query + " partition"]
    

    return render_to_response("result.html", locals())

