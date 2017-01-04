from django.contrib import admin

from .models import Query, GoogleResult, AlchemyResult

admin.site.register(Query)
admin.site.register(GoogleResult)
admin.site.register(AlchemyResult)
