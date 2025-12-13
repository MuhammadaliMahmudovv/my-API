from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUseradmin(admin.ModelAdmin):
    list_display = ["name", "email", "is_staff", "created_at"] 