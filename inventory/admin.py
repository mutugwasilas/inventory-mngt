from django.contrib import admin
from . models import Unit, Category, Inventory

# Register your models here.
admin.site.register(Unit)
admin.site.register(Category)
admin.site.register(Inventory)