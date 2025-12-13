from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not name:
            raise ValueError("User must have a name")
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password):
        if not name:
            raise ValueError("username is required")
        if not password:
            raise ValueError("password is required")
        user = self.model(name=name)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = []


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name
