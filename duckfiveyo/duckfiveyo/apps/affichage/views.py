from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from duckfiveyo.apps.annotation.dbspotlight import main
from duckfiveyo.apps.graphe.justin import graphRDF
from duckfiveyo.apps.mergeSimilarite.graphMerge import routineMatrice

from duckfiveyo.apps.recherche.recherche import get_result_google, get_result_alchemy

from .models import Query, GoogleResult, AlchemyResult

import json

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

    try:
        query_up = query.upper()
        model_query = Query.objects.get(query=query_up)
        g_result = json.loads(model_query.googleresult.result)
        a_result = get_result_alchemy(g_result)
        model_a_result = AlchemyResult(
            query=model_query,
            result=json.dumps(a_result)
        )
        model_a_result.save()
        # a_result = json.loads(model_query.alchemyresult.result)
        # print(g_result.__dict__)
        # a_result = model_query.alchemyresult.result
    except ObjectDoesNotExist:
        query_up = query.upper()
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


        # dico_mathieu, dico_view = routineQuery(query)
        print("ici")
    # googleResultView = json.dumps(dico_view)
    # googleResultMathieu = json.dumps(dico_mathieu)

        # model = GoogleResult(query=query, result=googleResultView, mathieu=googleResultMathieu)
        # model.save()
    
    # print(dico_view)

    # triplet = main(dico_mathieu)


    # dicoMilly = graphRDF(triplet)

    # queryList = [query,query+" cover",query+" partition",query+" album"]

    # resultfinal = routineMatrice(dicoMilly, queryList, 0.5)

    # web = resultfinal[query]
    # cover = resultfinal[query+" cover"]
    # album = resultfinal[query + " album"]
    # partition = resultfinal[query + " partition"]
    

    return render_to_response("result.html", locals())

