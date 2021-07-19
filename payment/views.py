from django.shortcuts import render, redirect
from django.urls import reverse
from django.template import context

from django.views.generic import View

from payment.forms import BillingAddressForm, PaymentMethodForm
from payment.models import BillingAddress
from order.models import Cart, Order

from django.contrib import messages

import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user)
        saved_address = saved_address[0]
        form = BillingAddressForm(instance=saved_address)
        payment_method_form = PaymentMethodForm()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = Order.objects.filter(user=request.user, ordered=False)
        order_totals = orders[0].get_totals()
        pay_meth = request.GET.get('pay_meth')
        context = {
            'form': form,
            'payment_method_form': payment_method_form,
            'carts': carts,
            'order_totals':order_totals,
            'pay_meth': pay_meth,
            'paypal_client_id': settings.PAYPAL_CLIENT_ID
        }
        return render(request, 'store/checkout.html', context)

    def post(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user)
        saved_address = saved_address[0]
        form = BillingAddressForm(instance=saved_address)
        pm_obj = Order.objects.filter(user=request.user, ordered=False)[0]
        pm_form = PaymentMethodForm(instance=pm_obj)
        if request.method == 'POST' or request.method == 'post':
            form = BillingAddressForm(request.POST, instance=saved_address)
            pm_form = PaymentMethodForm(request.POST, instance=pm_obj)
            if form.is_valid() and pm_form.is_valid():
                form.save()
                pay_method = pm_form.save()
                form = BillingAddressForm(instance=saved_address)
                # check if profile and billing address fully filled
                if not saved_address.is_fully_filled():
                    messages.info(request, "Please filledup Billing information to make payment!")
                    return redirect('payment:checkout')
                if not request.user.profile.is_fully_filled():
                    messages.info(request, "Please filledup account information to make payment!")
                    return redirect('account:customer_profile')

                # Cash On Delivery payment method Controlling
                if pay_method.payment_method == 'Cash On Delivery':
                    order_qs = Order.objects.filter(user=request.user, ordered=False)
                    order = order_qs[0]
                    order.ordered = True
                    order.orderId = order.id
                    order.paymentId = pay_method.payment_method
                    order.save()
                    cart_items = Cart.objects.filter(user=request.user, purchased=False)
                    for item in cart_items:
                        item.purchased = True
                        item.save()
                    print("Order Submited Successfully")
                    return redirect('store:index')
                if pay_method.payment_method == 'PayPal':
                    return redirect(reverse('payment:checkout') + "?pay_meth=" + str(pay_method.payment_method))



# Paypal payment method function
def PayPalPayment(request):
    data = json.loads(request.body)
    order_id = data['order_id']
    payment_id = data['payment_id']
    status = data['status']
    print(order_id)
    print(payment_id)
    print(status)
    if status == "COMPLETED":
        if request.user.is_authenticated:
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            order = order_qs[0]
            order.ordered = True
            order.orderId = order_id
            order.paymentId = payment_id
            order.save()
            cart_items = Cart.objects.filter(user=request.user, purchased=False)
            for item in cart_items:
                item.purchased = True
                item.save()
            return JsonResponse("Payment Submited!", safe=False)
    messages.success(request, "Your Order Under Processing..! ")
    return redirect('store:index')
