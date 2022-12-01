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
