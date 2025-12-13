# My API — Django REST API

## 📌 О проекте
Это backend-API, построенное на **Django + Django REST Framework + PostgreSQL + Docker**.  
Проект служит базой для REST-сервисов и демонстрирует работу с авторизацией, Docker-окружением и продакшн-подходом к настройке.

---

## 🚀 Возможности
✔ REST API для работы с пользователями  
✔ Docker + PostgreSQL  
✔ Переменные окружения через `.env`  
✔ Cоздание суперпользователя  
✔ JWT-аутентификация (access / refresh)  
✔ Защищённые эндпоинты

---

## 🛠 Технологии
- Python 3.12
- Django 6.0
- Django REST Framework (DRF)  
- PostgreSQL  
- Docker / Docker Compose

---

## 🧱 Архитектура
Проект организован в виде Django-приложения со следующими компонентами:
- models (пользователь)
- views (API)
- serializers
- URLs  
- Docker-окружение (В Docker-контейнере в качестве HOST используется `db`, а не `localhost`)

---

## 🔐 JWT Authentication
Проект использует JWT-аутентификацию (SimpleJWT).

Получение токена:
POST /api/token/

Пример тела запроса:
{
  "username": "admin",
  "password": "password"
}

Обновление токена:
POST /api/token/refresh/

Для доступа к защищённым эндпоинтам необходимо передавать заголовок:
Authorization: Bearer <access_token>

## 📦 Установка и запуск
```bash
1) Клонировать репозиторий
git clone https://github.com/MuhammadaliMahmudovv/my-API.git
cd my-API

2) Создать .env файл
Скопируй образец:
cp .env.example .env

Заполни переменные:
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://myuser:mypassword@localhost:5432/mydatabase

3) Запустить с Docker
docker compose down -v
docker compose up --build

4) Применить миграции (в контейнере)
docker compose exec web python manage.py migrate

Создать суперпользователя:
docker compose exec web python manage.py createsuperuser

