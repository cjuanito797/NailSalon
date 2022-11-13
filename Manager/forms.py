from django import forms
from django.core.validators import MinLengthValidator

STATE_OPTIONS = (
        ('Alabama', 'Alabama'),
        ('Alaska', 'Alaska'),
        ('Arizona', 'Arizona'),
        ('Arkansas', 'Arkansas'),
        ('California', 'California'),
        ('Colorado', 'Colorado'),
        ('Conneticut', 'Conneticut'),
        ('Deleware', 'Deleware'),
        ('Florida', 'Florida'),
        ('Georgia', 'Georgia'),
        ('Hawaii', 'Hawaii'),
        ('Idaho', 'Idaho'),
        ('Illinois', 'Illinois'),
        ('Indiana', 'Indiana'),
        ('Iowa', 'Iowa'),
        ('Kansas', 'Kansas'),
        ('Kentucky', 'Kentucky'),
        ('Louisiana', 'Louisiana'),
        ('Maine', 'Maine'),
        ('Maryland', 'Maryland'),
        ('Massachusetts', 'Massachusetts'),
        ('Michigan', 'Michigan'),
        ('Minnesota', 'Minnesota'),
        ('Mississippi', 'Mississippi'),
        ('Missouri', 'Missouri'),
        ('Montana', 'Montana'),
        ('Nebraska', 'Nebraska'),
        ('Nevada', 'Nevada'),
        ('New Hampshire', 'New Hampshire'),
        ('New Jersey', 'New Jersey'),
        ('New Mexico', 'New Mexico'),
        ('New York', 'New York'),
        ('North Carolina', 'North Carolina'),
        ('North Dakota', 'North Dakota'),
        ('Ohio', 'Ohio'),
        ('Oklahoma', 'Oklahoma'),
        ('Oregon', 'Oregon'),
        ('Pennsylvania', 'Pennsylvania'),
        ('Rhode Island', 'Rhode Island'),
        ('South Carolina', 'South Carolina'),
        ('South Dakota', 'South Dakota'),
        ('Tennessee', 'Tennessee'),
        ('Texas', 'Texas'),
        ('Utah', 'Utah'),
        ('Vermont', 'Vermont'),
        ('Virginia', 'Virgina'),
        ('Washington', 'Washington'),
        ('West Virginia', 'West Virginia'),
        ('Wisconsin', 'Wisconsin'),
        ('Wyoming', 'Wyoming'),
    )

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