from models import Person, Relationship

# Get the Person object associated with the logged-in user
def current_person(request):
    return get_person(request.user)

# From a user object, get the associated Person object.
def get_person(user):
    return Person.objects.get(user=user)

# Get a list of the user's friends
def confirmed_friends(person):
    friends = []
    r1 = Relationship.objects.filter(requester=person, confirmed=True)
    friends += [rel.requested for rel in r1]
    r2 = Relationship.objects.filter(requested=person, confirmed=True)
    friends += [rel.requester for rel in r2]
    return friends

# Get a list of people the user has requested
def requested_friends(person):
    friends = []
    r = Relationship.objects.filter(requester=person, confirmed=False)
    friends += [rel.requested for rel in r]
    return friends


