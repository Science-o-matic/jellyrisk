from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from accounts.models import UserProfile

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileInlineAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]

class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ["user", "name", "surname", "email",
                    "recieve_newsletter", "participate_in_contest",
                    "is_staff"]
    list_filter =  ["recieve_newsletter", "participate_in_contest"]

admin.site.register(User, UserProfileInlineAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
