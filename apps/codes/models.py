from django.db import models
from ..list import models as shopping_cart
from ..inventory import models as inventory


class AbstractCode(models.Model):
    code = models.CharField(max_length=50, blank=True, unique=True)
    initial_date = models.DateTimeField(auto_now_add=True)
    is_inventory = models.BooleanField(default=False, blank=True)
    is_shopping_cart = models.BooleanField(default=False, blank=True)


class CodeShoppingCart(AbstractCode):
    shopping_cart = models.ForeignKey(shopping_cart.ShoppingCart,
                                      on_delete=models.CASCADE)


class CodeInventory(AbstractCode):
    inventory = models.ForeignKey(inventory.Inventory,
                                  on_delete=models.CASCADE)
