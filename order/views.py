from django.shortcuts import render, get_object_or_404, redirect
#messages
from django.contrib import messages
# authentications
from django.contrib.auth.decorators import login_required
#model
from order.models import Cart, Order
from store.models import Product, VariationValue


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, vendor=item.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            size = request.POST.get('size')
            color = request.POST.get('color')
            quantity = request.POST.get('quantity')
            if quantity:
                order_item[0].quantity += int(quantity)
            else:
                order_item[0].quantity += 1
            order_item[0].size = size
            order_item[0].color = color
            order_item[0].save()
            messages.info(request, "This item quantity was updated!")
            return redirect('store:index')
        else:
            size = request.POST.get('size')
            color = request.POST.get('color')
            order.orderitems.add(order_item[0])
            order.vendor.add(order_item[0].vendor)
            order_item[0].size = size
            order_item[0].color = color
            order_item[0].save()
            messages.info(request, "This item was added to your cart!")
            return redirect('store:index')
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        order.vendor.add(order_item[0].vendor)
        messages.info(request, "This item was added to your cart!")
        return redirect('store:index')



@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        context = {
            'carts': carts,
            'order': order
        }
        return render(request, 'store/cart.html', context)
    else:
        messages.warning(request, "You don't have any item in your cart!")
        return redirect('store:index')



@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was remove from your cart!")
            return redirect('order:cart')
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('store:index')
    else:
        messages.info(request, "You don't have an active order")
        return redirect('store:index')


@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return redirect('order:cart')
        else:
            messages.info(request, f"{item.name} is not in your cart")
            return redirect('store:index')
    else:
        messages.info(request, "You don't have an active order")
        return redirect('store:index')



@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return redirect('order:cart')
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} item has been removed from your cart")
                return redirect('order:cart')
        else:
            messages.info(request, f"{item.name} is not in your cart")
            return redirect('store:index')
    else:
        messages.info(request, "You don't have an active order")
        return redirect('store:index')