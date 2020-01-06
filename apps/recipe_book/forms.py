from django import forms
from . import models


class RecipeForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = (
            'name',
            'cooking_time',
            'tips',
            'image',
            'review',
        )
        labels = {
            'name': 'Nombre de la receta',
            'cooking_time': 'Tiempo de preparación de la receta',
            'tips': 'Consejos',
            'image': 'Imagen de referencia',
            'review': 'Hacer que mi receta sea pública (será'
                      ' revisada por un administrador)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre de la '
                                                          'receta'}),
            'cooking_time': forms.TextInput({'placeholder': 'Tiempo de '
                                                            'preparación'}),
            'tips': forms.Textarea(attrs={'placeholder': 'Tips y consejos '
                                                         'para preparar la '
                                                         'receta'}),

            'image': forms.ClearableFileInput(attrs={'placeholder': 'imagen '
                                                                    'de la '
                                                                    'receta'}),
            'review': forms.CheckboxInput(attrs={'label': 'Hacer que mi '
                                                          'receta sea pública '
                                                          '(será revisada por '
                                                          'un administrador'})
        }


RecipeStepFormSet = forms.modelformset_factory(
    models.RecipeStep,
    fields=('instruction',),
    labels={'instruction': 'Pasos a seguir'},
    widgets={
        'instruction': forms.Textarea(attrs={'placeholder': 'Escriba aqui el '
                                                            'paso a seguir'})
    })

RecipeItemFormSet = forms.modelformset_factory(
    models.RecipeItem,
    fields=('quantity', 'product'),
    labels={'quantity': 'cantidad', 'product': 'Ingrediente'},
    widgets={
        'quantity': forms.TextInput(attrs={'placeholder': 'cantidad'}),
        'product': forms.TextInput(attrs={'placeholder': 'Ingrediente'})
    })
