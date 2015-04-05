"""
This file contains code that listens for signals and acts on them
"""
from django.dispatch import receiver

from registration import signals

from models import Person

# Handles the "user_registered" signal that comes from the registration app.
# Creates a new Person when a new User registers for the site
@receiver(signals.user_registered)
def handle_user_registered(sender, user, request, **kwargs):
    Person.objects.create(user=user)
