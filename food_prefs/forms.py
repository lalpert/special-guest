from django.forms import ModelForm
from models import Person

# Form for a Person to edit their preferences
class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['preference_text']
