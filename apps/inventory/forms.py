from .models import Inventory, InventoryProduct
from django.forms import ModelForm, TextInput


class InventoryForm(ModelForm):

    class Meta:
        model = Inventory
        fields = {
            'name',
        }
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Nombre del Inventario'}),
        }


class InventoryProductForm(ModelForm):

    class Meta:
        model = InventoryProduct
        fields = {
            'product',
        }

    def save(self, inventory_id=None, commit=True):
        product = super().save(commit=False)
        product.inventory = Inventory.objects.get(id=inventory_id)
        if commit:
            product.save()
        return product
