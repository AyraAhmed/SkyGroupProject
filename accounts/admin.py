from django.contrib import admin
from .models import UserProfile

# register the UserProfile model so it appears in Django admin 
admin.site.register(UserProfile)
