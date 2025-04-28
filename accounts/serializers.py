from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

# Serializer for Django's built in User model 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True} # Don't expose password in API responses 
        }

    # custom update method to handle password properly
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password) # Hash the new password securely
        instance.save()
        return instance

# Serializer for the extended UserProfile model
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer() # Nest the UserSerializer inside 

    class Meta:
        model = UserProfile
        fields = ['user', 'role', 'phone_number']

    # custom update to handle nested User and UserProfile updates 
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()

        # update the instance fields with the validated data 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
