from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from duckfiveyo.apps.annotation.dbspotlight import main
from duckfiveyo.apps.graphe.graphRDF import graphRDF
from duckfiveyo.apps.mergeSimilarite.graphMerge import routineMatrice

from duckfiveyo.apps.recherche.recherche import get_result_google, get_result_alchemy

from .models import Query, GoogleResult, AlchemyResult, FinalResult

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
        tout = json.loads(model_query.finalresult.tout)
        partition = json.loads(model_query.finalresult.partition)
        cover = json.loads(model_query.finalresult.cover)

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
    
        partition = {}
        for key, value in a_result["quentin"].items():
            if value["info"]["tab"] or value["info"]["partition"]:
                partition[key] = g_result[key]

        # for key, result in a_result["quentin"].items():
        #     pprint.pprint(result)
        # triplet = main(a_result)

        categories = ["cover", "partition", "tablature", "chords"]

        dico = graphRDF(a_result["mathieu"])

        dico_milly = routineMatrice(dico, categories)

        pprint.pprint(dico_milly)

        cover_url_list = dico_milly[categories[0]]
        partition_url_list = dico_milly[categories[1]]
        tab_url_list = dico_milly[categories[2]]
        chords_url_list = dico_milly[categories[3]]


        cover = []

        for url in cover_url_list:
            cover.append(g_result[url])

        for url in partition_url_list:
            partition[url] = g_result[url]
        
        for url in tab_url_list:
            partition[url] = g_result[url]
        
        for url in chords_url_list:
            partition[url] = g_result[url]

        
        tout = order_result(g_result)

        f_result = FinalResult(
            query=model_query,
            tout=json.dumps(tout),
            cover=json.dumps(cover),
            partition=json.dumps(partition)
        )
        f_result.save()
    
    #   print(triplet)

    # dicoMilly = graphRDF(triplet)

    # queryList = [query,query+" cover",query+" partition",query+" album"]

    # resultfinal = routineMatrice(dicoMilly, queryList, 0.5)

    # web = resultfinal[query]
    # cover = resultfinal[query+" cover"]
    # album = resultfinal[query + " album"]
    # partition = resultfinal[query + " partition"]
    except MultipleObjectsReturned:
        # remove ceux qui sont vide
        print("ici")
        pass
    

    return render_to_response("result.html", locals())

def order_result(dico):
    result_list = []
    other = []
    other2 = []

    for key,value in dico.items():
        if "wikipedia".upper() in value["title"].upper() or "wikipédia".upper() in value["title"].upper():
            result_list.append(value)
        else:
            other.append(value)
        
    for value in other:
        if "youtube".upper() in value["title"].upper():
            result_list.append(value)
        else:
            other2.append(value)
        
    return result_list + other2

