# AUTHOR OF THIS PAGE AYRA AHMED W1947450
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import VoteLog, ViewSummary
from datetime import date

# signal to create a ViewSummary automatically when a new VoteLog is saved
@receiver(post_save, sender=VoteLog)
def create_view_summary(sender, instance, created, **kwargs):
    if created:
        # debug message for confirming signal trigger 
        print(" Signal fired: creating ViewSummary") 
        ViewSummary.objects.create(
            view_type=instance.vote_type,
            view_date=date.today(),
            progress=100,
            vote_log=instance,
            session=instance.session
        )
