# AUTHOR OF THIS PAGE AYRA AHMED W1947450
from django.db import models
from accounts.models import UserProfile

# Models for health check 
class Team(models.Model):
    id = models.IntegerField(db_column='TeamID', primary_key=True)
    name = models.CharField(db_column='TeamName', max_length=50, unique=True)
    size = models.CharField(db_column='TeamSize', max_length=50)

    class Meta: 
        db_table = 'Team'

    def __str__(self):
        return self.name # display the team name in admin or shell 

class Session(models.Model):
    session_date = models.DateField()
    session_time = models.TimeField()

    def __str__(self):
        return f"{self.session_date} {self.session_time}" # show date and time together 

class HealthCard(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name # display the health card's name 
    
class VoteLog(models.Model):
    STATUS_CHOICES = [
        ('Stable', 'Stable'),
        ('Improving', 'Improving'),
        ('Getting worse', 'Getting worse'),
    ]

    vote_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    comment = models.CharField(max_length=50, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    health_card = models.ForeignKey(HealthCard, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{self.status} - {self.health_card.name}" # show status and health card name 
    

class ViewSummary(models.Model):
    view_type = models.CharField(max_length=50)
    view_date = models.DateField()
    progress = models.IntegerField()
    vote_log = models.ForeignKey(VoteLog, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Summary on {self.view_date}" # display the view summary date 
    