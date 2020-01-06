from django.db import models
from apps.items.models import Product
from django.contrib.auth.models import User


class Recipe(models.Model):
    name = models.CharField(max_length=150, null=False)
    cooking_time = models.CharField(max_length=20, null=True)
    tips = models.TextField(null=True, blank=True, max_length=200)
    image = models.ImageField(width_field=300, height_field=300, blank=True,
                              null=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    public = models.BooleanField(default=False, blank=True)
    review = models.BooleanField(default=False, blank=True)


class RecipeStep(models.Model):
    step_order = models.SmallIntegerField(null=False, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    instruction = models.TextField(null=False, blank=False)
    optional = models.BooleanField(blank=True, default=False)

    def __str__(self):
        optional = '(Opcional) ' if self.optional is True else ''
        return "{}{}".format(optional, self.instruction)


class RecipeItem(models.Model):
    product = models.ForeignKey(Product, null=True,
                                on_delete=models.SET_DEFAULT,
                                default=None)
    quantity = models.CharField(max_length=50, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    notes = models.TextField(max_length=200, default='', blank=True)
