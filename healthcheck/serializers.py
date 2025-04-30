# AUTHOR OF THIS PAGE AYRA AHMED W1947450
from rest_framework import serializers
from .models import ViewSummary

# Serializer for displaying a summary view of votes 
class ViewSummarySerializer(serializers.ModelSerializer):
     # Get health card name from related vote_log 
    card = serializers.CharField(source='vote_log.health_card.name')
    # Get status from related vote_log 
    status_label = serializers.CharField(source='vote_log.status')
    # dynamically set colour based on the status 
    status_color = serializers.SerializerMethodField()
    # get optional comment from vote_log 
    feedback = serializers.CharField(source='vote_log.comment', allow_null=True)

    # determining the colour based on vote status 
    def get_status_color(self, obj):
        color_map = {
            'Stable': 'green', 
            'Improving': 'amber',
            'Getting worse': 'red'
        }
        # default to grey if status is not found 
        return color_map.get(obj.vote_log.status, 'grey')
    
class Meta:
    model = ViewSummary
    fields = ['card', 'status_label', 'status_color', 'feedback'] # fields exposed in API 