from django import forms
from django.db.models import fields

from payment.models import BillingAddress
from order.models import Order


class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ('__all__')
        exclude = ('user',)



class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_method', ]