from django import template

from account.models import User
from store.models import Category, Product

register = template.Library()

@register.filter
def product_count(user):
    total_product = Product.objects.filter(user=user)
    if total_product.exists():
        return total_product.count()
    else:
        return 0


