from django.db import models
from django.contrib.auth.models import User
import datetime


class Person(models.Model):
    preference_text = models.TextField()
    user = models.OneToOneField(User)
    def __unicode__(self):
        return unicode(self.user)


class Relationship(models.Model):
    requester = models.ForeignKey(Person,related_name="requester")
    requested = models.ForeignKey(Person,related_name="requested")
    confirmed = models.BooleanField(default=False)
    #created = models.DateField(default=datetime.date.today)
    def __unicode__(self):
        return unicode(self.requester) + ", " + unicode(self.requested)


