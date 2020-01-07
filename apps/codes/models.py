from django.db import models
from ..list import models as shopping_cart
from ..inventory import models as inventory
from datetime import datetime
from .. import constants as cnst, utils


class AbstractCode(models.Model):
    code = models.CharField(max_length=50, blank=True, unique=True)
    initial_date = models.DateTimeField(auto_now_add=True)
    is_inventory = models.BooleanField(default=False, blank=True)
    is_shopping_cart = models.BooleanField(default=False, blank=True)

    def _create_code(self, pk):
        inv = 1 if self.is_inventory else 0
        cart = 1 if self.is_shopping_cart else 0

        code = '{}{}{}{}'.format(inv, cart, pk, datetime.now().strftime(
            '%y%m%w%I%M%S'))
        print(code)
        return code

    def is_outdated(self):
        delta = utils.time_delta(self.initial_date, cnst.LIVE_CODE_DEFAULT)
        print(delta)
        return True if delta > cnst.LIVE_CODE else False

    def __str__(self):
        return self.code


class CodeShoppingCart(AbstractCode):
    shopping_cart = models.ForeignKey(shopping_cart.ShoppingCart,
                                      on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.is_shopping_cart = True
            self.code = self._create_code(kwargs['id_object'])
            kwargs = {}
        super(CodeShoppingCart, self).save(*args, **kwargs)


class CodeInventory(AbstractCode):
    inventory = models.ForeignKey(inventory.Inventory,
                                  on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        print(kwargs)
        if self.pk is None:
            self.is_inventory = True
            self.code = self._create_code(kwargs['id_object'])
            kwargs = {}
        super(CodeInventory, self).save(*args, **kwargs)
