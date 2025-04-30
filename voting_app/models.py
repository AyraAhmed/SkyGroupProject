from django.db import models
from django.contrib.auth.models import User

class HealthCard(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    health_card = models.ForeignKey(HealthCard, on_delete=models.CASCADE)
    rating = models.CharField(max_length=10, choices=[('red', 'Red'), ('amber', 'Amber'), ('green', 'Green')])
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'health_card']

    def __str__(self):
        return f"{self.user} voted {self.rating} for {self.health_card}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[
        ('engineer', 'Engineer'),
        ('team_leader', 'Team Leader'),
        ('department_leader', 'Department Leader')
    ])

    def __str__(self):
        return f"{self.user.username} - {self.role}"
