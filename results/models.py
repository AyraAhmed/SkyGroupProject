from django.db import models
from accounts.models import UserProfile
from healthcheck.models import VoteLog, ViewSummary

# Create your models here.
class Record(models.Model):
    record_type = models.CharField(max_length=50)
    record_historical = models.CharField(max_length=50)
    view_summary = models.ForeignKey(ViewSummary, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.record_type} - {self.user_profile.user.username} - {self.view_summary.view_date}"





