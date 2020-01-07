from datetime import datetime
from django.conf import settings
from . import constants


# FIXME: entender como funcionan los canales privados
#  https://blog.rmotr.com/the-definitive-django-pusher-guide-dfe2fb8117cc


def create_channel_name(obj, name):
    """
    Crea un nombre de canal a partir de el tipo de objeto que necesita y el
    nombre del objeto a crear

    :param obj: nombre de tipo objeto que lo crea
    :param name: nombre asignado a la instancia que lo crea

    :return: Nombre para el canal
    """
    channel_name = 'private-{}{}{}'.format(datetime.now().timestamp(), obj,
                                           name)

    if len(channel_name) > settings.PUSHER_CHANNEL_MAX_LENGTH:
        channel_name = channel_name[:164]

    return channel_name


def time_delta(origin, unit='sec'):
    delta_secs = (datetime.utcnow() - origin.replace(
        tzinfo=None)).total_seconds()
    if unit == 'sec':
        return delta_secs
    elif unit == 'min':
        return delta_secs/constants.SECONDS_MINUTE
    elif unit == 'hour':
        return delta_secs/constants.SECONDS_HOUR
    else:
        return delta_secs/constants.SECONDS_DAY

