from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
import util
from forms import PersonForm
from models import Relationship, Person

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            pass
    else:
        pass
        # Return an 'invalid login' error message.

def index(request):
    if request.user.is_authenticated():
        return logged_in_homepage(request)
    else:
        return logged_out_homepage(request)

def logged_in_homepage(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def logged_out_homepage(request):
    template = loader.get_template('logged_out_homepage.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def view_profile(request):
    template = loader.get_template('view_profile.html')
    d = {"person": util.current_person(request)} 
    context = RequestContext(request, d)
    return HttpResponse(template.render(context))

def edit_profile(request):
    person = util.current_person(request)

    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        form.save()
    else:
        form = PersonForm(instance=person)

    d = {
        "person": person,
        "form": form
        } 

    template = loader.get_template('edit_profile.html')
    context = RequestContext(request, d)
    return HttpResponse(template.render(context))

def all_friends(request):
    person = util.current_person(request)
    friends = util.confirmed_friends(person)

    d = {
        "person": person,
        "friends": friends
        } 

    template = loader.get_template('view_friends.html')
    context = RequestContext(request, d)
    return HttpResponse(template.render(context))

def find_friends(request):
    person = util.current_person(request)
    
    if request.method == "POST":
        requested_id = int(request.POST["requested_id"])
        requested = Person.objects.get(id=requested_id)
        # TODO change to false and add a way to confirm friends
        rel = Relationship.objects.create(requester=person, requested=requested, confirmed=True) 

    confirmed_friends = util.confirmed_friends(person)
    requested_friends = util.requested_friends(person)
    all_people = Person.objects.exclude(id=person.id)
    for p in all_people:
        if p in confirmed_friends:
            p.confirmed_friend = True
        elif p in requested_friends:
            p.requested_friend = True

    d = {
        "person": person,
        "all_people": all_people
        } 

    template = loader.get_template('find_friends.html')
    context = RequestContext(request, d)
    return HttpResponse(template.render(context))


