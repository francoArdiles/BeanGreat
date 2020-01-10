from django.db import models
from django.contrib.auth.models import User
from ..items.models import Product
from django.conf import settings
from django.urls import reverse
from ..utils import create_channel_name


class Inventory(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE,
                              related_name='inventory_owner_set')
    users = models.ManyToManyField(User)
    channel_name = models.CharField(max_length=settings.
                                    PUSHER_CHANNEL_MAX_LENGTH, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.channel_name = create_channel_name('inv', self.name)
        super(Inventory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('inventory', args=[str(self.id)])

    def __str__(self):
        return self.name

    def count_items(self):
        return self.inventoryproduct_set.all().count()

    def count_users(self):
        return self.users.all().count()

    def usernames(self):
        users = [u.username for u in self.users.all()]
        return users


class InventoryProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, default=1)

    def __str__(self):
        return str(self.product)
