# 📌 My API — Django REST API

REST API для управления пользователями и профилями с аутентификацией JWT, реализованное с помощью Django и Django REST Framework (DRF).

---

## 🧠 Описание

Проект представляет собой backend-API, написанное на Django + Django REST Framework и использует PostgreSQL и Docker для удобного запуска. Реализован современный подход к авторизации через JWT и бизнес-endpoint’ы (`me`, `change_password`) для реального использования.

Основные возможности:

✔ Регистрация пользователя  
✔ JWT авторизация (access + refresh)  
✔ Защищённые эндпоинты  
✔ Ограничения доступа по ролям (admin / обычный пользователь)  
✔ Бизнес-endpoint’ы (`me`, `change_password`)  
✔ Docker-окружение  

---

## 🛠 Технологии

- Python 3.12  
- Django 6.0  
- Django REST Framework  
- PostgreSQL  
- Docker / Docker Compose  
- JWT Authentication (simplejwt)

---

## 📦 Установка и запуск
1. Клонировать репозиторий
```bash
git clone https://github.com/MuhammadaliMahmudovv/my-API.git
cd my-API
```
2. Создать .env файл
Скопируй (.env.example → .env) и заполни:
```bash
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://postgres:24132315@db:5432/myapi_db
```
- В Docker-окружении HOST=db, а не localhost.

3. Запустить Docker-окружение
```bash
docker compose down -v
docker compose up --build
```

4. Применить миграции
```bash
docker compose exec web python manage.py migrate
```

5. Создать суперпользователя (опционально)
```bash
docker compose exec web python manage.py createsuperuser
```

🔐 JWT Authentication
Получение токена:
```bash
POST /api/token/


Body:
{
  "username": "your_username",
  "password": "your_password"
}


Ответ:
{
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN"
}
```

Обновление токена
```bash
POST /api/token/refresh/
```

Body:
```bash
{
  "refresh": "<REFRESH_TOKEN>"
}
```

Использование токена
Для всех защищённых запросов передавай в заголовке:
```bash
Authorization: Bearer <ACCESS_TOKEN>
```
