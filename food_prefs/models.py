from django.db import models
from django.contrib.auth.models import User
import datetime


# Represents a user of the system. Contains a Django User object as well as extra information.
class Person(models.Model):
    preference_text = models.TextField("Enter your preferences/restrictions")
    user = models.OneToOneField(User)
    def __unicode__(self):
        return unicode(self.user)


# Represents a relationship between two people - either friends or pending friends
class Relationship(models.Model):
    # Person who requested the friendship
    requester = models.ForeignKey(Person,related_name="requester")
    # Person who was requested
    requested = models.ForeignKey(Person,related_name="requested")
    # Whether the friendship has been confirmed by both parties - if False, this is a pending friendship.
    confirmed = models.BooleanField(default=False)
    def __unicode__(self):
        return unicode(self.requester) + ", " + unicode(self.requested)


