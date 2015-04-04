"""
This file contains code that listens for signals
"""
from django.dispatch import receiver

from registration import signals

from models import Person


@receiver(signals.user_registered)
def handle_user_registered(sender, user, request, **kwargs):
    Person.objects.create(user=user)
