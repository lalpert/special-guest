from models import Person, Relationship

# Get the Person object associated with the logged-in user
def current_person(request):
    return get_person(request.user)

# From a user object, get the associated Person object.
def get_person(user):
    return Person.objects.get(user=user)

# Confirm the friendship
def accept_friend(requester, requested):
    request = Relationship.objects.get(requester=requester, requested=requested)
    request.confirmed = True
    request.save()

# Get a list of the person's friends
def confirmed_friends(person):
    friends = []
    r1 = Relationship.objects.filter(requester=person, confirmed=True)
    friends += [rel.requested for rel in r1]
    r2 = Relationship.objects.filter(requested=person, confirmed=True)
    friends += [rel.requester for rel in r2]
    print "Confirmed friends", friends
    return friends

# Get a list of people the person has requested
def requested_friends(person):
    friends = []
    r = Relationship.objects.filter(requester=person, confirmed=False)
    friends += [rel.requested for rel in r]
    return friends

# Get a list of people who have requested this person as a friend
def have_requested(person):
    friends = []
    r = Relationship.objects.filter(requested=person, confirmed=False)
    friends += [rel.requester for rel in r]
    return friends

# Return a list of all people, with information on if they are a confirmed or
# pending friend of the given Person.
def get_all_people_with_annotations(person):
    confirmed = confirmed_friends(person)
    requested = requested_friends(person)
    requested_me = have_requested(person)
    all_people = Person.objects.exclude(id=person.id)
    for p in all_people:
        if p in confirmed:
            p.confirmed_friend = True
        elif p in requested:
            p.requested_friend = True
        elif p in requested_me:
            p.requested_me = True

    return all_people

