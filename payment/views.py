from django.shortcuts import render, redirect
from django.template import context

from django.views.generic import View

from payment.forms import BillingAddressForm, PaymentMethodForm
from payment.models import BillingAddress
from order.models import Cart, Order

from django.contrib import messages

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        form = BillingAddressForm()
        payment_method_form = PaymentMethodForm()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = Order.objects.filter(user=request.user, ordered=False)
        order_totals = orders[0].get_totals()
        context = {
            'form': form,
            'payment_method_form': payment_method_form,
            'carts': carts,
            'order_totals':order_totals
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
                # if not saved_address.is_fully_filled():
                #     messages.info(request, "Please fillup Billing information to make payment!")
                #     return redirect('payment:checkout')
                # if not request.user.profile.is_fully_filled():
                #     messages.info(request, "Please fillup account information to make payment!")
                #     return redirect('payment:checkout')

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