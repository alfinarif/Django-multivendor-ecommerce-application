from django.db.models import fields
from django.forms.models import ModelForm

from store.models import Category, Product

from order.models import Cart

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')
        exclude = ('user','parent',)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')
        exclude = ('user','category',)

