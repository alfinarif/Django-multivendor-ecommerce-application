from django.db import models
from django.urls.base import reverse
from account.models import User
from django.shortcuts import reverse


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_base_category')
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    image = models.ImageField(upload_to='category', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Categories'



class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_base_product')
    name = models.CharField(max_length=255, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    preview_des = models.TextField(max_length=200, verbose_name='Preview Description')
    description = models.TextField(max_length=1000, verbose_name="Description")
    image = models.ImageField(upload_to='products', blank=False, null=False)
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    is_stock = models.BooleanField(default=True)
    is_slider = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("store:product_detail", kwargs={"pk": self.pk})
    

    class Meta:
        ordering = ['-created']

    
class VariationManager(models.Manager):
    def sizes(self):
        return super(VariationManager, self).filter(variation='size')

    def colors(self):
        return super(VariationManager, self).filter(variation='color')

VARIATIONS = (
    ('size', 'size'),
    ('color', 'color'),
)

class VariationValue(models.Model):
    variation = models.CharField(max_length=100, choices=VARIATIONS)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.IntegerField()

    objects = VariationManager()

    def __str__(self) -> str:
        return self.name