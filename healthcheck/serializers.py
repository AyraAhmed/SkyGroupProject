from rest_framework import serializers
from .models import ViewSummary

class ViewSummarySerializer(serializers.ModelSerializer):
    card = serializers.CharField(source='vote_log.health_card.name')
    status_label = serializers.CharField(source='vote_log.status')
    status_color = serializers.SerializerMethodField()
    feedback = serializers.CharField(source='vote_log.comment', allow_null=True)

    def get_status_color(self, obj):
        color_map = {
            'Stable': 'green', 
            'Improving': 'amber',
            'Getting worse': 'red'
        }
        return color_map.get(obj.vote_log.status, 'grey')
    
class Meta:
    model = ViewSummary
    fields = ['card', 'status_label', 'status_color', 'feedback']