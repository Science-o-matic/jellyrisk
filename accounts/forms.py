from registration.forms import RegistrationForm
from django import forms


class UserProfileRegistrationForm(RegistrationForm):
    recieve_newsletter = forms.BooleanField(required=False)
    participate_in_contest = forms.BooleanField(required=False)
