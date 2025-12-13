from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path("user-list/", views.CustomUserList, name="user_list"),
    path("user-list/<int:pk>/", views.CustomUserDetailView, name="user_detail_view"),
    path("user-create/", views.CustomUserCreate, name="user_create"),
    path("user-update/", views.CustomUserUpdate, name="user-update"),
    path("user-delete/<int:pk>", views.CustomUserDelete, name="user_delete"),
    path("protected/", views.ProtectedHello.as_view(), name="protected"),
    path("profile-list/", views.ProfileList, name="profiles"),
    # -
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
]
