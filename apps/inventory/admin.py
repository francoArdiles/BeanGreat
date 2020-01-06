from django.contrib import admin
from .models import Inventory, InventoryProduct

# Register your models here.

admin.site.register(Inventory)
admin.site.register(InventoryProduct)
