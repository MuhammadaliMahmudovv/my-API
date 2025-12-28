from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    BasePermission,
)

from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsOwnerOrAdmin
from .paginations import PostPagination
from .models import CustomUser, Profile, Posts
from .serializers import (
    CustomUserSerializer,
    ProfileSerializer,
    RegistrationSerializer,
    ChangePasswordSerializer,
    PostsSerializer,
)


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.all().order_by("-created_at")
        return CustomUser.objects.filter(is_staff=False).order_by("-created_at")

    def get_permissions(self):
        if self.action == "me":
            return [IsAuthenticated()]
        if self.action == "list":
            return [IsAuthenticated()]
        if self.action == "create":
            return [IsAdminUser()]
        return [IsAuthenticated, IsOwnerOrAdmin]

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
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "register_limit"

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "User created"}, status=status.HTTP_201_CREATED)


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = []
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    search_fields = ["title"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated, IsOwnerOrAdmin]

    @action(
        detail=False,
        url_path="my-posts",
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def my_posts(self, request):
        queryset = self.get_queryset().filter(author=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


"""
# ------------------------------------------------------------------------------------------------------------------------


ModelViewSet по умолчанию включает операции:
- list: список всех объектов
- retrieve: просмотр одного объекта
- create: создание объекта
- update/partial_update: изменение объекта
- destroy: удаление объекта

Метод: get_queryset() --> Какие данные вернуть.
Метод: get_permissions() --> Кто имеет доступ.


1. Основные атрибуты (Статика)
Эти переменные задают базовое поведение «по умолчанию».
queryset — базовый набор данных, который будет использоваться.
serializer_class — основной класс сериализатора.
permission_classes — список прав доступа (на весь ViewSet).
pagination_class — класс для настройки пагинации.
lookup_field — поле, по которому ищется объект (по умолчанию 'pk').

2. Динамические методы (Логика выбора)
Используются, когда нужно менять поведение «на лету» (например, в зависимости от роли пользователя).


- def get_queryset(self):
Определяет, какие записи увидит пользователь.
Зачем: Скрыть чужие записи, показать только активные товары и т.д.
Пример: return Book.objects.filter(owner=self.request.user)

- get_serializer_class(self)
Выбирает разные сериализаторы для разных действий.
Зачем: В списке (list) показывать краткую информацию, а в деталях (retrieve) — полную.
Пример: if self.action == 'list': 
            return CompactSerializer return FullSerializer

- get_permissions(self)
Настраивает доступ для каждого действия отдельно.
Зачем: Просмотр разрешить всем, а создание — только админам.
Пример: return [IsAdminUser()] if self.action == 'create' else [AllowAny()]

- get_object(self)
Возвращает один конкретный объект.
Зачем: Если логика поиска объекта в базе сложнее, чем просто «найти по ID».


# ------------------------------------------------------------------------------------------------------------------------


DRF = 3 уровня защиты

Authentication
→ кто ты? (JWT, request.user)

Permission
→ можно ли тебе в принципе сюда?

Queryset / Object permission
→ какие данные ты видишь


# ------------------------------------------------------------------------------------------------------------------------


Docker.

1) docker-compose up — Запуск. Создает и запускает все контейнеры, описанные в файле. Выводит логи прямо в консоль.
2) docker-compose up -d — Запуск в фоне. То же самое, но освобождает терминал (контейнеры работают в фоновом режиме).
3) docker-compose down — Остановка и удаление. Выключает контейнеры и полностью удаляет их (а также общие сети, созданные для проекта). Данные в Volume при этом сохраняются.
4) docker-compose up --build — Пересборка и запуск. Принудительно пересобирает образы перед запуском. Нужно использовать, если вы внесли изменения в Dockerfile или исходный код, которые должны попасть в образ.
5) docker-compose exec web [команда] — Выполнение внутри. Позволяет запустить команду внутри уже работающего контейнера web.
   - Пример: docker-compose exec web bash — зайти в терминал контейнера.
   

# ------------------------------------------------------------------------------------------------------------------------


@action — это способ добавить бизнес-endpoint в ViewSet,
который не является стандартным CRUD-действием.

### Какие бывают @action:

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


### Параметры конфигурации эндпоинта:

1.
methods: Список HTTP-методов (строчными буквами).
methods=['post'] — только POST.
methods=['get', 'delete'] — разрешить несколько методов.
По умолчанию: ['get'].

2.
permission_classes: Список классов прав доступа.
Позволяет переопределить глобальные права только для этого действия. Например, весь ViewSet доступен всем, а change-password — только [IsAuthenticated].

3.
throttle_classes: Классы ограничения частоты запросов.
То, что мы обсуждали ранее. Позволяет задать отдельный лимит именно для этой функции (например, лимит на попытки ввода пароля).

4.
serializer_class: Переопределение сериализатора.
Если для этого действия нужны другие поля (например, для смены пароля нужен сериализатор с полями old_password и new_password, а не стандартный UserSerializer).

5.
url_path: Имя в URL-адресе.

6.
По умолчанию берется название функции (заменяя _ на -).
Если функция называется set_password, путь будет /set-password/. Если задать url_path='change', путь станет /change/.

url_name: Имя для внутреннего именования (для функции reverse).


### Как переопределить настройки внутри метода

Иногда нужно динамически менять поведение прямо в коде. Внутри метода @action вам доступны:
self.get_object(): Вернет объект, если detail=True.
self.get_queryset(): Вернет текущий набор данных.
self.get_serializer(*args, **kwargs): Создаст экземпляр сериализатора, который указан в serializer_class (или стандартный для ViewSet).


# ------------------------------------------------------------------------------------------------------------------------


throttle_classes = [ScopedRateThrottle]: Ты явно указываешь, что для этого эндпоинта нужно использовать именно ScopedRateThrottle. Это переопределяет глобальные настройки для этого View.
throttle_scope = "register_limit": Это «мостик» к настройкам. DRF видит эту строку, идет в settings.py, находит там register_limit и понимает: «Ага, здесь лимит 3 запроса в час».


# ------------------------------------------------------------------------------------------------------------------------
"""
