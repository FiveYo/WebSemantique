from django.conf.urls import include, url
from django.contrib import admin

from .views import home, ask

urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^result', ask, name="result"),
]