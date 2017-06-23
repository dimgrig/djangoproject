from django.db import models
from products.models import Product
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return ("Статус {}").format(self.name)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

class Order(models.Model):

    user = models.ForeignKey(User, blank=True, null=True, default=None)


    customer_name = models.CharField(max_length=128, blank=True, null=True, default=None)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=48, blank=True, null=True, default=None)
    customer_address = models.CharField(max_length=128, blank=True, null=True, default=None)
    comments = models.TextField(max_length=200, blank=True, null=True, default=None)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # nmb*price_per_item ?? ???? products
    status = models.ForeignKey(Status)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return ("Заказ {} : {}").format(self.id, self.status.name)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0) # nmb*price_per_item
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return ("Товар в заказе {}").format(self.product.id)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товаров в заказе"

    def save(self, *args, **kwargs):
        self.price_per_item = self.product.price
        self.amount = int(self.nmb)*float(self.price_per_item)

        super(ProductInOrder, self).save(*args, **kwargs)

def products_in_order_post_save(sender, instance, created, **kwargs):

    total_price = 0
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)
    for item in all_products_in_order:
        total_price += item.amount

    instance.order.total_price = total_price
    instance.order.save(force_update=True)

post_save.connect(products_in_order_post_save, sender=ProductInOrder)

class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0) # nmb*price_per_item
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return ("Товар в корзине {}").format(self.product.id)

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товаров в корзине"

    def save(self, *args, **kwargs):
        self.price_per_item = self.product.price
        self.amount = int(self.nmb) * self.price_per_item

        super(ProductInBasket, self).save(*args, **kwargs)
