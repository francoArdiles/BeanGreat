from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .. import constants
# TODO expandir modelo de usuario
# Agregar:
# preferencias alimenticias done
# Recetas favoritas         done
# Listas de compras


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    food_restriction = models.CharField(choices=constants.FOOD_TYPES,
                                        max_length=2, default=constants.OMNIVORE,
                                        blank=True)


# This will ensure the profile is made when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
