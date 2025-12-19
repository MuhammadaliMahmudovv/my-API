from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import CustomUser, Profile
from .serializers import (
    CustomUserSerializer,
    ProfileSerializer,
    RegistrationSerializer,
    ChangePasswordSerializer,
)
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
# ------------------------------------------------------------


ModelViewSet по умолчанию включает операции:
- list: список всех объектов
- retrieve: просмотр одного объекта
- create: создание объекта
- update/partial_update: изменение объекта
- destroy: удаление объекта

Метод: get_queryset() --> Какие данные вернуть.
Метод: get_permissions() --> Кто имеет доступ.


# ------------------------------------------------------------


DRF = 3 уровня защиты

Authentication
→ кто ты? (JWT, request.user)

Permission
→ можно ли тебе в принципе сюда?

Queryset / Object permission
→ какие данные ты видишь


# ------------------------------------------------------------


Docker.

1) docker-compose up — Запуск. Создает и запускает все контейнеры, описанные в файле. Выводит логи прямо в консоль.
2) docker-compose up -d — Запуск в фоне. То же самое, но освобождает терминал (контейнеры работают в фоновом режиме).
3) docker-compose down — Остановка и удаление. Выключает контейнеры и полностью удаляет их (а также общие сети, созданные для проекта). Данные в Volume при этом сохраняются.
4) docker-compose up --build — Пересборка и запуск. Принудительно пересобирает образы перед запуском. Нужно использовать, если вы внесли изменения в Dockerfile или исходный код, которые должны попасть в образ.
5) docker-compose exec web [команда] — Выполнение внутри. Позволяет запустить команду внутри уже работающего контейнера web.
   - Пример: docker-compose exec web bash — зайти в терминал контейнера.
   

# ------------------------------------------------------------


@action — это способ добавить бизнес-endpoint в ViewSet,
который не является стандартным CRUD-действием.

Какие бывают @action:

1. detail=False (действие над системой)
@action(detail=False, methods=["get"])
def me(self, request):
    ...

URL:
/users/me/

2. detail=True (действие над объектом)
@action(detail=True, methods=["post"])
def block(self, request, pk=None):
    ...
    
URL:
/users/12/block/

Примеры бизнес-endpoint'ов

@action(detail=False)
def me(self, request): ...

@action(detail=False, methods=["post"])
def change_password(self, request): ...

@action(detail=True, methods=["post"])
def deactivate(self, request, pk=None): ...

@action(detail=True, methods=["post"])
def promote(self, request, pk=None): ...


# ------------------------------------------------------------
"""


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.all().order_by("-created_at")
        return CustomUser.objects.filter(is_staff=False).order_by("-created_at")

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]
        if self.action == "create":
            return [IsAdminUser()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="change-password",
    )
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"detail": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"detail": "Password changed successfully"}, status=status.HTTP_200_OK
        )

    """
    detail=False: Это значит, что URL будет выглядеть как /users/change-password/.
    Если бы было True, URL требовал бы ID: /users/{id}/change-password/.
     Поскольку пользователь меняет свой собственный пароль, ID в ссылке не нужен.
    """

    """
    check_password — это встроенный метод модели пользователя в Django, предназначенный для безопасной аутентификации. 
    Его главная задача: проверить, соответствует ли введенный пользователем текст («сырой» пароль) зашифрованному паролю, который хранится в базе данных.
    
    --- Как это работает (Техническая часть)
    В базе данных пароли никогда не хранятся в открытом виде. Там находится хеш (например: pbkdf2_sha256$260000$salt$hash).
    Когда вы вызываете user.check_password("мой_пароль"):
    Извлечение: Django берет из объекта user его текущий хеш.
    Анализ: Он считывает из этого хеша алгоритм шифрования и уникальную «соль» (случайную строку, добавленную при регистрации).
    Хеширование: Django берет введенный вами текст "мой_пароль", добавляет к нему ту же самую «соль» и прогоняет через тот же алгоритм.
    Сравнение: Метод сравнивает полученный результат с тем, что лежит в базе. Если они идентичны — пароль верный.
    
    Шпаргалка для разработчика
    1. Синтаксис: Метод вызывается только у экземпляра (объекта) пользователя.
        результат = user.check_password("введенный_текст")
    2. Что возвращает:
        True: Если пароль подошел.
        False: Если пароль неверный или вместо пароля передано пустое значение (None)
    """


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "User created"}, status=status.HTTP_201_CREATED)
