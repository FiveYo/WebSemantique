from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render_to_response

from duckfiveyo.apps.recherche.search import routineQuery

from duckfiveyo.apps.annotation.dbspotlight import main

from .models import GoogleResult

from duckfiveyo.apps.graphe.justin import graphRDF

from duckfiveyo.apps.mergeSimilarite.graphMerge import routineMatrice

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

    # try:
    #     result = GoogleResult.objects.get(query=query)
    #     dico_mathieu = result.mathieu
    #     dico_view = result.result

    # except Exception:
    dico_mathieu, dico_view = routineQuery(query)

    # googleResultView = json.dumps(dico_view)
    # googleResultMathieu = json.dumps(dico_mathieu)

        # model = GoogleResult(query=query, result=googleResultView, mathieu=googleResultMathieu)
        # model.save()
    
    # print(dico_view)

    triplet = main(dico_mathieu)


    dicoMilly = graphRDF(triplet)

    queryList = [query,query+" cover",query+" partition",query+" album"]

    resultfinal = routineMatrice(dicoMilly, queryList, 0.5)

    web = resultfinal[query]
    cover = resultfinal[query+" cover"]
    album = resultfinal[query + " album"]
    partition = resultfinal[query + " partition"]
    

    return render_to_response("result.html", locals())

