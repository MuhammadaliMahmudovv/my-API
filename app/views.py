from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import CustomUser, Profile
from .serializers import CustomUserSerializer, ProfileSerializer, RegistrationSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    BasePermission,
)

"""
ModelViewSet по умолчанию включает операции:
- list: список всех объектов
- retrieve: просмотр одного объекта
- create: создание объекта
- update/partial_update: изменение объекта
- destroy: удаление объекта

Метод: get_queryset() --> Какие данные вернуть.
Метод: get_permissions() --> Кто имеет доступ.


# --


DRF = 3 уровня защиты

Authentication
→ кто ты? (JWT, request.user)

Permission
→ можно ли тебе в принципе сюда?

Queryset / Object permission
→ какие данные ты видишь
"""


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_staff=False).order_by("-created_at")
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]
        if self.action == "create":
            return [IsAdminUser()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "User created"}, status=status.HTTP_201_CREATED)
