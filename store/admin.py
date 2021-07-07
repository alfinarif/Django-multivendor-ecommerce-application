from django.contrib import admin

from store.models import Category, Product, VariationValue

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(VariationValue)