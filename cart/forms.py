from django import forms


SERVICE_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddServiceForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=SERVICE_QUANTITY_CHOICES,
                                coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)