from django.db import models
from accounts.models import UserProfile
from healthcheck.models import VoteLog, ViewSummary

# Model for storing historical records linked to view summaries and users
class Record(models.Model):
    record_type = models.CharField(max_length=50)
    record_historical = models.CharField(max_length=50)
    view_summary = models.ForeignKey(ViewSummary, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        # showing a readable description combining record type, username, and view date
        return f"{self.record_type} - {self.user_profile.user.username} - {self.view_summary.view_date}"




# class Record(models.Model):
#     team = models.CharField(max_length=100)
#     department = models.CharField(max_length=100)
#     progress_month = models.IntegerField()  # e.g., 3, 6, 9
#     red_count = models.IntegerField(default=0)
#     yellow_count = models.IntegerField(default=0)
#     green_count = models.IntegerField(default=0)

#     def __str__(self):
#         return f"{self.team} - {self.department} - {self.progress_month} months"



