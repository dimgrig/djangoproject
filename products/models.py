from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True, default=None)

    def __str__(self):
        return ("Категория {}").format(self.name)

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

class Product(models.Model):

    name = models.CharField(max_length=128, blank=True, null=True, default=None)
    description = models.TextField(max_length=500, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.IntegerField(default=0)
    category = models.ForeignKey(ProductCategory, blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return ("Товар {}").format(self.name)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class ProductImage(models.Model):

    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    image = models.ImageField(upload_to='products_images/')
    is_active = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return ("{}").format(self.id)

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"
