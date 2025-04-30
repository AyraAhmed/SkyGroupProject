from django.db import models

class SeniorManagerResult(models.Model):
    team_name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    progress_month = models.IntegerField()  # 3, 6, or 9
    traffic_signal = models.CharField(max_length=10)  # Red, Yellow, Green
    count = models.IntegerField()

    def __str__(self):
        return f"{self.team_name} - {self.department_name} - {self.progress_month} months - {self.traffic_signal}: {self.count}"
  

class DepartmentLeaderResult(models.Model):
    TEAM_CHOICES = [
        ('Team Alpha', 'Team Alpha'),
        ('Team Beta', 'Team Beta'),
        ('Team Gamma', 'Team Gamma'),
    ]
    DEPARTMENT_CHOICES = [
        ('Department 1', 'Department 1'),
        ('Department 2', 'Department 2'),
    ]
    HEALTHCARD_CHOICES = [
        ('Delivery value', 'Delivery value'),
        ('Easy to release', 'Easy to release'),
        ('fun', 'fun'),
        ('health of codebase', 'health of codebase'),
        ('learning', 'learning'),
        ('mision', 'mision'),
        ('pawns or players', 'pawns or players'),
        ('speed', 'speed'),
        ('suitable process', 'suitable process'),
        ('support', 'support'),
        ('teamwork', 'teamwork'),
        ('work life', 'work life'),
    ]
    PROGRESS_CHOICES = [
        (3, 'Progress after 3 Months'),
        (6, 'Progress after 6 Months'),
        (9, 'Progress after 9 Months'),
    ]
    TRAFFIC_CHOICES = [
        ('Red', 'Red'),
        ('Yellow', 'Yellow'),
        ('Green', 'Green'),
    ]

    team = models.CharField(max_length=50, choices=TEAM_CHOICES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    healthcard = models.CharField(max_length=100, choices=HEALTHCARD_CHOICES)
    progress_month = models.IntegerField(choices=PROGRESS_CHOICES)
    traffic_signal = models.CharField(max_length=10, choices=TRAFFIC_CHOICES)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.team} - {self.department} - {self.healthcard} - {self.progress_month}m - {self.traffic_signal}: {self.count}"
