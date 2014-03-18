from django import forms
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationForm


class UserProfileRegistrationForm(RegistrationForm):
    recieve_newsletter = forms.BooleanField(
        required=False, initial=True,
        label=_("Recieve newsletter")
    )
    participate_in_contest = forms.BooleanField(
        required=False,
        label=_("Participate in jellyfish photo contest")
    )
