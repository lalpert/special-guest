from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
from django.contrib import messages
import util
from forms import PersonForm
from models import Relationship, Person

# Set this to True to let people add friends with no confirmation.
# Set it to False to make the other person have to confirm the friendship
CONFIRM_FRIENDS_AUTOMATICALLY = True


def add_extra_info(request, context_dict):
    person = util.current_person(request)
    context_dict["num_requests"] = len(util.have_requested(person))

def render_with_extra_info(request, context_dict, template_name):
    add_extra_info(request, context_dict)
    template = loader.get_template(template_name)
    context = RequestContext(request, context_dict)
    return HttpResponse(template.render(context))

# Main page at /
def index(request):
    if request.user.is_authenticated():
        return logged_in_homepage(request)
    else:
        return logged_out_homepage(request)

# Homepage shown to logged-in users
def logged_in_homepage(request):
    return render_with_extra_info(request, {}, 'index.html')

# Homepage shown to logged-out users
def logged_out_homepage(request):
    template_name = 'logged_out_homepage.html'
    template = loader.get_template(template_name)
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


# Displays the logged-in user's profile
def view_profile(request):
    d = {"person": util.current_person(request)} 
    return render_with_extra_info(request, d, 'view_profile.html')

# Lets a user edit their profile
def edit_profile(request):
    person = util.current_person(request)

    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        form.save()
        return redirect('your_profile')

    else:
        form = PersonForm(instance=person)

    d = {
        "person": person,
        "form": form
        } 

    return render_with_extra_info(request, d, 'edit_profile.html')

# Display a list of the current user's friends
def all_friends(request):
    person = util.current_person(request)

    if request.method == "POST":
        requester_id = int(request.POST["requester_id"])
        requester = Person.objects.get(id=requester_id)
        util.accept_friend(requester, person)

    friends = util.confirmed_friends(person)
    pending_friends = util.have_requested(person) 

    d = {
        "person": person,
        "friends": friends,
        "pending_friends": pending_friends,
        } 

    return render_with_extra_info(request, d, 'view_friends.html')

# Display all users and let current user add them as friends
def find_friends(request):
    person = util.current_person(request)
    
    if request.method == "POST":
        print "POST:", request.POST
        if request.POST["type"] == "request":
            requested_id = int(request.POST["requested_id"])
            requested = Person.objects.get(id=requested_id)
            rel = Relationship.objects.create(requester=person, 
                    requested=requested, confirmed=CONFIRM_FRIENDS_AUTOMATICALLY) 
            messages.success(request, 'You have requested %s' % requested.user.username)
        elif request.POST["type"] == "accept":
            requester_id = int(request.POST["requester_id"])
            requester = Person.objects.get(id=requester_id)
            util.accept_friend(requester, person)
            messages.success(request, 'You are now friends with %s' % requester.user.username)
            
        
    # Get all People with info on their friendship with current user
    all_people = util.get_all_people_with_annotations(person)
   
    d = {
        "person": person,
        "all_people": all_people
        } 

    return render_with_extra_info(request, d, 'find_friends.html')
