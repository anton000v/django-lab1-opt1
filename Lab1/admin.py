from django.contrib import admin
from . import models


class ProductModelAdmin(admin.ModelAdmin):
    class Meta:
        model = models.Product

admin.site.register(models.Product, ProductModelAdmin)
