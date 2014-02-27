from django.db import models
from django.contrib.auth.models import User
from registration.signals import user_registered


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='profile')
    recieve_newsletter = models.BooleanField(default=True, null=False, blank=False)
    participate_in_contest = models.BooleanField(default=False, null=False, blank=False)

    def __unicode__(self):
        return unicode(self.user)

def user_registered_callback(sender, user, request, **kwargs):
    profile = UserProfile(user = user)
    profile.recieve_newsletter = bool(request.POST.get("recieve_newsletter", False))
    profile.participate_in_contest = bool(request.POST.get("participate_in_contest", False))
    profile.save()

user_registered.connect(user_registered_callback)
