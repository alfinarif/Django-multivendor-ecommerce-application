from django.db import models
from django.conf import settings
from store.models import Product, VariationValue


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} X {self.item}'

    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total, '0.2f')
        return float_total
    
    def variation_total(self):
        variation = VariationValue.objects.filter(variation='size', product=self.item)
        colors = VariationValue.objects.filter(variation='color', product=self.item)
        for variant in variation:
            if colors.exists():
                for color in colors:
                    if color.name == self.color:
                        c_price = color.price
                        color_quantity_price = c_price * self.quantity
                if variant.name == self.size:
                    total = variant.price * self.quantity
                    net_total = total + color_quantity_price
                    float_total = format(net_total, '0.2f')
                    return float_total
            else:
                if variant.name == self.size:
                    total = variant.price * self.quantity
                    float_total = format(total, '0.2f')
                    return float_total

    
    def variation_single_price(self):
        variation = VariationValue.objects.filter(variation='size', product=self.item)
        colors = VariationValue.objects.filter(variation='color', product=self.item)
        for variant in variation:
            if colors.exists():
                for color in colors:
                    if color.name == self.color:
                        c_price = color.price
                if variant.name == self.size:
                    total = variant.price + c_price
                    net_total = total
                    float_total = format(net_total, '0.2f')
                    return float_total
            else:
                if variant.name == self.size:
                    total = variant.price
                    float_total = format(total, '0.2f')
                    return float_total


PAYMENT_METHOD = (
    ('Cash On Delivery', 'Cash On Delivery'),
    ('PayPal', 'PayPal'),
    ('SSLCommerz', 'SSLCommerz')
)

class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vendor = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='vendor_order')
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264, blank=True, null=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)
    vendor_total = models.FloatField(default=0.00)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD, default="Cash On Delivery")

    def __str__(self) -> str:
        return f"{self.user.email} Orders"

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            if order_item.variation_total():
                total += float(order_item.variation_total())
            elif order_item.variation_single_price():
                total += float(order_item.variation_single_price())
            else:
                total += float(order_item.get_total())

        return total
    

