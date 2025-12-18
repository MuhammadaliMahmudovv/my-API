from django.contrib import admin
from .models import CustomUser, Profile

@admin.register(CustomUser)
class CustomUseradmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_staff", "created_at"] 
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "age"]