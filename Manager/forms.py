from django import forms

class AppointmentID(forms.Form):
    id = forms.CharField(label='id')