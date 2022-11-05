from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.forms import modelformset_factory
from .models import User
from django.core.exceptions import ValidationError
from django.forms import HiddenInput
from django.forms.models import ModelForm


class RegistrationForm (UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email', 'password1', 'password2', 'first_name', 'last_name', 'street_num', 'city', 'state', 'zipcode', 'phoneNumber')

    def __init__(self, *args, **kwargs):
        super (RegistrationForm, self).__init__ (*args, **kwargs)

        for visible in self.visible_fields ( ):
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

        for fieldname in ['password1', 'password2', ]:
            self.fields[fieldname].help_text = None

class LoginForm (forms.Form):
    email = forms.CharField ( )
    password = forms.CharField (widget=forms.PasswordInput)

class EditAddress (forms.ModelForm):
    class Meta:
        model = User

        fields = ("street_num", "city", "state", "zipcode")

class EmailChangeForm(forms.Form):
    new_email1 = forms.EmailField(
        label=("New email address"),
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label=("New email address confirmation"),
        widget=forms.EmailInput,
    )
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)
    def clean_new_email1(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')
        if new_email1 and old_email:
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                )
        return new_email1
    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )
        return new_email2

    def save(self, commit=True):
        email = self.cleaned_data["new_email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user