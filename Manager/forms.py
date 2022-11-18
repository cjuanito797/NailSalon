from django import forms
from django.core.validators import MinLengthValidator

SCHEDULE_CHOICES = (
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
    ('saturday', 'Saturday'),
    ('sunday', 'Sunday'),
)

class NewTechnicianForm(forms.Form):
    email = forms.EmailField (max_length=254)
    scheduled_day = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=SCHEDULE_CHOICES)

'''
class NewTechnicianForm(forms.Form):
    email = forms.EmailField (max_length=254)
    first_name = forms.CharField (max_length=200)
    last_name = forms.CharField (max_length=200)
    street_num = forms.CharField (max_length=20)
    city = forms.CharField (max_length=20)
    state = forms.CharField (max_length=15, widget=forms.Select(choices=STATE_OPTIONS))
    zipcode = forms.CharField (max_length=5, validators=[MinLengthValidator (5)])
    phone_number = forms.CharField (max_length=10, validators=[MinLengthValidator (10)])
    scheduled_day = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=SCHEDULE_CHOICES)
    '''