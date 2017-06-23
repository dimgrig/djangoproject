from django.contrib import admin
from .models import *

class ProductsImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0 #дополнительные поля

class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    inlines = [ProductsImageInline]
    class Meta:
        model = Product


class ProductImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]

    class Meta:
        model = ProductImage

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]

    class Meta:
        model = ProductCategory

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)

