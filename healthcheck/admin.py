from django.contrib import admin
from .models import Team, Session, HealthCard, VoteLog, ViewSummary
# add models to Django Admin
admin.site.register(Team)
admin.site.register(Session)
admin.site.register(HealthCard)
admin.site.register(VoteLog)
admin.site.register(ViewSummary)