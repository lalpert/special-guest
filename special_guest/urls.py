from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^food_prefs/', include('food_prefs.urls')),
    url(r'^$', 'food_prefs.views.index'),

    # Login/register via django's built-in auth sytem.
    # See https://docs.djangoproject.com/en/1.7/topics/auth/default/#module-django.contrib.auth.views
    # url('^', include('django.contrib.auth.urls')),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),

    # do i need this?
)
