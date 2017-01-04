from django.db import models

class Query(models.Model):
    """
    Représente une Query simple "Starway to heaven"
    """
    query = models.TextField()

class GoogleResult(models.Model):
    """
    Associé à une Query, la variable *result* contient le json retourné par google
    """
    query = models.OneToOneField(Query)

    """
    result = {
        "http://... ": {
            url: "http://",
            title: "Titre present sur google",
            snippet: "description breve de ce qu'il y a sur l'url",
        }
    }
    """
    result = models.TextField()


class AlchemyResult(models.Model):
    """
    Associé à une Query, la variable *result* contient le texte retourné par alchemy
    """
    query = models.OneToOneField(Query)

    """
    result = { "http://..." : "150 premiers mots venant de AlchemyAPI" }
    """
    result = models.TextField()
