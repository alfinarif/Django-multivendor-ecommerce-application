from django.contrib import admin

from account.models import User, Profile, BecomeSeller

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(BecomeSeller)
