from rest_framework import serializers
from .models import HealthCard, Vote, UserProfile
from django.contrib.auth.models import User

class HealthCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCard
        fields = ['id', 'name', 'description']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'health_card', 'rating', 'feedback', 'user']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'role']
        read_only_fields = ['user']
