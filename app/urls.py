from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

router = DefaultRouter()
router.register(r"users-list", views.CustomUserViewSet, basename="users-list")
router.register(r"profiles-list", views.ProfileViewSet, basename="profiles-list")
router.register(r"posts", views.PostsViewSet, basename="post-list")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    # -
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
]
