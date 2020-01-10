from .models import ShoppingCart, ShoppingProduct
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


class ShoppingProductForm(ModelForm):

    class Meta:
        model = ShoppingProduct
        fields = (
            'product',
            'quantity',
            'note',
        )
        widgets = {
            'quantity': TextInput(attrs={'value': 1, 'min': 1,
                                         'type': 'number'}),
        }

    def save(self, container_id=None, commit=True):
        product = super().save(commit=False)
        product.list = ShoppingCart.objects.get(id=container_id)
        if commit:
            product.save()
        return product
