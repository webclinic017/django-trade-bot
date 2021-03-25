from django.contrib import admin
from django.contrib import auth

from .models import User, Team 

# Register your models here.

#admin.site.unregister(auth.models.User)
#admin.site.unregister(auth.models.Group)

admin.site.register(User)
#admin.site.register(Group)
admin.site.register(Team)