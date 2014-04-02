import os
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from registration.signals import user_registered, user_activated


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='profile')
    recieve_newsletter = models.BooleanField(default=True, null=False, blank=False)
    participate_in_contest = models.BooleanField(default=False, null=False, blank=False)

    def is_staff(self):
        return bool(self.user.is_staff)

    def email(self):
        return self.user.email

    def name(self):
        return self.user.name

    def surname(self):
        return self.user.surname

    def __unicode__(self):
        return unicode(self.user)


def user_registered_callback(sender, user, request, **kwargs):
    profile = UserProfile(user=user)
    profile.recieve_newsletter = bool(request.POST.get("recieve_newsletter", False))
    profile.participate_in_contest = bool(request.POST.get("participate_in_contest", False))
    profile.save()


def user_activated_callback(sender, user, request, **kwargs):
    if user.get_profile().participate_in_contest:
        email = EmailMessage(
            "Jellyfish Photography Competition 2014",
            "Welcome to the Jellyfish Photography Competition 2014.\n"
            "Please find attached the Rules and Guidelines of the Contest "
            "available in english, spanish, italian, french, maltese, "
            "catalan and arabic",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],

        )
        email.attach_file(
             os.path.join(
                 settings.STATIC_ROOT,
                 'pdf/med_jellyrisk_jellyfish_photography_competition_2014.pdf'
             )
        )
        email.send()


user_registered.connect(user_registered_callback)
user_activated.connect(user_activated_callback)
