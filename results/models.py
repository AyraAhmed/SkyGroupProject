from django.db import models

class SeniorManagerResult(models.Model):
    team_name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    progress_month = models.IntegerField()  # 3, 6, or 9
    traffic_signal = models.CharField(max_length=10)  # Red, Yellow, Green
    count = models.IntegerField()

    def __str__(self):
        return f"{self.team_name} - {self.department_name} - {self.progress_month} months - {self.traffic_signal}: {self.count}"
