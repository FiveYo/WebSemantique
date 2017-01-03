from django.db import models


class GoogleResult(models.Model):
    query = models.TextField()
    result = models.TextField()
    mathieu = models.TextField()
