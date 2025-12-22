from rest_framework import serializers
from .models import CustomUser, Profile, Posts


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "name", "email", "created_at"]


class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()
    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "age"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ["name", "email", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user



class PostsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Posts
        fields = ["user", "title", "description"]