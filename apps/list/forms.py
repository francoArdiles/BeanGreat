from .models import ShoppingCart
from django.forms import ModelForm, TextInput


class ShoppingCartForm(ModelForm):

    class Meta:
        model = ShoppingCart
        fields = {
            'name',
        }
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Nombre de la lista'}),
        }
