from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, blank=True)
    role = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    team = models.ForeignKey('healthcheck.Team', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.user.username  #  This is what Django admin uses
