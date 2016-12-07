from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render_to_response

from duckfiveyo.apps.annotation.dbspotlight import annotations

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

    liste = annotations(query, "", "")

    return render_to_response("result.html", locals())

