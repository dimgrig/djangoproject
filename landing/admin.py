from django.contrib import admin
from .models import *

class SubscirberAdmin(admin.ModelAdmin):
    list_display = {"name", "email"}
    list_display = [field.name for field in Subscirber._meta.fields]
    list_filter = ["name"] #фильтрация по полю
    search_fields = ["name", "email"] #поиск по полю
    #exclude = ["email"] #???хз
    #inlines

    class Meta:
        model = Subscirber


# Register your models here.
admin.site.register(Subscirber, SubscirberAdmin)
