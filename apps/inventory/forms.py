from .models import Inventory
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
