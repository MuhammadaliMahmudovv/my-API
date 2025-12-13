from rest_framework import serializers
from .models import CustomUser, Profile


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "name", "email", "created_at"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user", "bio", "age"]