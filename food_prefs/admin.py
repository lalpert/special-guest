from django.contrib import admin
from food_prefs import models

# Register models to show up in admin site
admin.site.register(models.Person)
admin.site.register(models.Relationship)
