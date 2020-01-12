from .models import ShoppingCart, ShoppingProduct
from django import forms


class ShoppingCartForm(forms.ModelForm):

    class Meta:
        model = ShoppingCart
        fields = {
            'name',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre de la '
                                                          'lista'}),
        }


class ShoppingProductForm(forms.ModelForm):

    class Meta:
        model = ShoppingProduct
        fields = (
            'product',
            'quantity',
            'note',
        )
        widgets = {
            'quantity': forms.TextInput(attrs={'value': 1, 'min': 1,
                                               'type': 'number'}),
        }

    def save(self, container_id=None, commit=True):
        product = super().save(commit=False)
        product.list = ShoppingCart.objects.get(id=container_id)
        if commit:
            product.save()
        return product


class NewShoppingCart(forms.Form):
    add_to_shopping_cart = forms.ChoiceField(required=True)
    name = forms.CharField(max_length=50, required=False)
    products = forms.CheckboxSelectMultiple()
