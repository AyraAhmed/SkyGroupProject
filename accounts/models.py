from django.db import models
from django.contrib.auth.models import User

# User model from SQLite database with additional profile information like phone number 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, blank=True)
    role = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    team = models.ForeignKey('healthcheck.Team', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.user.username  #  defining string representation, used in Django Admin

# class Department(models.Model):
#     department_id = models.AutoField(primary_key=True)  # Matches DepartmentID
#     department_name = models.CharField(max_length=50, unique=True)  # Matches DepartmentName
#     number_of_teams = models.CharField(max_length=50)  # Matches NumberOfTeams
#     user_profile = models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True,blank=True)  # Matches UserProfileID

#     def __str__(self):
#         return self.department_name
