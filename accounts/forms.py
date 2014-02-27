from registration.forms import RegistrationForm
from django import forms


class UserProfileRegistrationForm(RegistrationForm):
    recieve_newsletter = forms.BooleanField(required=False, initial=True)
    participate_in_contest = forms.BooleanField(required=False)
