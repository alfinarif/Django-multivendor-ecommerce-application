from django import template
from django.contrib.admin.decorators import register

from order.models import Cart, Order

register = template.Library()

@register.filter
def hover_cart_count(user):
    cart = Cart.objects.filter(user=user, purchased=False)
    if cart.exists():
        return cart.count()
    else:
        return 0

@register.filter
def hover_cart_view(user):
    cart = Cart.objects.filter(user=user, purchased=False)[:3]
    if cart.exists():
        return cart
    else:
        return cart


@register.filter
def hover_cart_total(user):
    orders = Order.objects.filter(user=user, ordered=False)
    if orders.exists():
        order = orders[0]
        return order.get_totals()
    else:
        return 0

