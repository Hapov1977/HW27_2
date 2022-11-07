from django.contrib import admin

from ads.models import AdModel, CatModel, LocationModel

admin.site.register(AdModel)
admin.site.register(CatModel)
admin.site.register(LocationModel)