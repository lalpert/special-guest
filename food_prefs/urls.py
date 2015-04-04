from django.conf.urls import patterns, url

from food_prefs import views

# Just need this to make sure receivers get activated as soon as the project starts up
import receivers

urlpatterns = patterns('',
    # Main index page
    url(r'^$', views.index, name='index'),

    # View your own profile
    url(r'^profile$', views.view_profile, name='your_profile'),

    # Edit your profile
    url(r'^edit_profile$', views.edit_profile, name='edit_profile'),

    # User profile, e.g. /food_prefs/user/5/
    url(r'^user/(?P<person_id>\d+)/$', views.view_profile, name='user_profile'),

    # All your friends, e.g. /food_prefs/all_friends/
    url(r'^all_friends$', views.all_friends, name='view_friends'),

    # Find and add friends
    url(r'^find_friends$', views.find_friends, name='find_friends'),


)
