from django.db import models
from ..items.models import Product, CustomProduct
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from ..utils import create_channel_name


class ShoppingCart(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE,
                              related_name='shopping_cart_owner_set')
    users = models.ManyToManyField(User)
    channel_name = models.CharField(max_length=settings.
                                    PUSHER_CHANNEL_MAX_LENGTH, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.channel_name = create_channel_name('list', self.name)
        super(ShoppingCart, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shopping_cart', args=[str(self.id)])

    def count_items(self):
        total = self.shoppingcustomproduct_set.count() + \
                self.shoppingproduct_set.count()
        return total

    def count_users(self):
        return self.users.all().count()

    def usernames(self):
        users = [u.username for u in self.users.all()]
        return users


class ShoppingProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(default=0, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    note = models.TextField(max_length=150, blank=True, null=True,
                            editable=True)
    list = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    bought = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return str(self.product)

    def save(self, *args, **kwargs):
        # Fixme: si item ya existe, solo actualizar la cantidad
        super(ShoppingProduct, self).save(*args, **kwargs)


class ShoppingCustomProduct(CustomProduct):
    price = models.IntegerField(default=0, blank=True)
    list = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    bought = models.BooleanField(default=False, blank=True)
