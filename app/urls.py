from django.urls import path
from . import views

urlpatterns = [
    path("user-list/", views.CustomUserList, name="user_list"),
    path("user-list/<int:pk>/", views.CustomUserDetailView, name="user_detail_view"),
    path("user-create/", views.CustomUserCreate, name="user_create"),
    path("user-update/", views.CustomUserUpdate, name="user-update"),
    path("user-delete/<int:pk>", views.CustomUserDelete, name="user_delete"),
]
