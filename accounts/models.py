from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='profile')
    recieve_newsletter = models.BooleanField(default=True, null=False, blank=False)
    participate_in_contest = models.BooleanField(default=False, null=False, blank=False)

    def __unicode__(self):
        return self.user
