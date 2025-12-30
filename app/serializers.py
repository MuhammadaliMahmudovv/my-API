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


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]
        
    def validate_avatar(self, file):
        if not file.content_type.startswith("image/"):
            raise serializers.ValidationError("Только изображения")
        if file.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Файл слишком большой")
        return file


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ["name", "email", "password"]

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Имя слишком корокое!")
        if "admin" in value.lower():
            raise serializers.ValidationError("Имя не может содержать слово 'admin'.")
        return value

    def validate_email(self, value):
        if value in CustomUser.objects.values_list("email", flat=True):
            raise serializers.ValidationError(
                "Этот адрес электронной почты уже используется."
            )
        return value

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


"""

Если вам нужен просто список строк, используйте метод values_list. Параметр flat=True превращает список кортежей в обычный список значений.
# Получаем плоский список: ['user1@mail.com', 'user2@mail.com', ...]
emails = CustomUser.objects.values_list('email', flat=True)

for email in emails:
    print(email)
    
    
"""
