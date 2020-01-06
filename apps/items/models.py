from django.db import models
from apps.constants import FOOD_TYPES


class Pasillo(models.Model):
    name = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=150, null=False)
    brand = models.CharField(max_length=100, null=True, blank=True)
    food_type = models.CharField(choices=FOOD_TYPES, max_length=2, null=True,
                                 blank=True)

    def __str__(self):
        return self.name


class CustomProduct(Item):
    note = models.TextField(blank=True, null=True)


class Product(Item):
    aisle = models.ForeignKey(Pasillo, null=True, on_delete=models.SET_NULL)
