# Лабораторная работа №1 — Simple Blog API

Проект **Simple Blog API** представляет собой RESTful API для упрощённой блог-платформы, реализованной на **FastAPI**.
Приложение поддерживает управление пользователями, статьями и комментариями, а также реализует JWT-аутентификацию и работу с базой данных PostgreSQL.

Проект задеплоен на **[Render.com](https://render.com/)** и доступен по ссылке на документацию:
🔗 **[Swagger UI — Simple Blog API](https://microservice-architecture.onrender.com/docs#)**

## Основной стек технологий

* **Python 3.13**
* **FastAPI** — веб-фреймворк для построения RESTful API
* **SQLAlchemy + AsyncPG** — асинхронная ORM для работы с PostgreSQL
* **Alembic** — инструмент для миграций базы данных
* **Pydantic** — валидация данных и конфигурации
* **Python-JOSE** — реализация JWT-аутентификации
* **Docker + Docker Compose** — контейнеризация и изоляция окружения
* **GitHub Actions + GHCR + Render** — CI/CD и автоматический деплой

## Архитектура проекта

Проект реализован в архитектурном шаблоне **MVC (Model-View-Controller)** и имеет следующую структуру:

```
src/
├── core/
│   ├── errors/            # Глобальные обработчики ошибок
│   ├── utils/             # JWT, аутентификация и генерация slug
├── models/                # SQLAlchemy-модели (User, Article, Comment)
├── schemas/               # Pydantic-схемы для запросов и ответов
├── controllers/           # Логика бизнес-операций
├── routes/                # Определение маршрутов FastAPI
├── main.py                # Точка входа в приложение
└── db.py                  # Подключение к базе данных
migrations/                # Миграции Alembic
```

## Функционал API

### Управление пользователями

* `POST /api/users` — регистрация нового пользователя
* `POST /api/users/login` — аутентификация и получение JWT
* `GET /api/user` — получение текущего пользователя
* `PUT /api/user` — обновление профиля

### Управление статьями

* `POST /api/articles` — создание статьи
* `GET /api/articles` — получение списка статей
* `GET /api/articles/{slug}` — получение статьи по slug
* `PUT /api/articles/{slug}` — обновление статьи
* `DELETE /api/articles/{slug}` — удаление статьи

### Управление комментариями

* `POST /api/articles/{slug}/comments` — добавление комментария
* `GET /api/articles/{slug}/comments` — получение всех комментариев к статье
* `DELETE /api/articles/{slug}/comments/{id}` — удаление комментария

## Настройка и запуск проекта

### Вариант 1: Локальный запуск без Docker

1. Клонируйте репозиторий и создайте виртуальное окружение:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux / macOS
   venv\Scripts\activate         # Windows
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Создайте базу данных PostgreSQL (пример через psql):

   ```bash
   psql -U postgres
   CREATE DATABASE blog_db;
   ```

4. Скопируйте файл окружения:

   ```bash
   cp .env.example .env
   ```

5. В `.env` измените переменную `DATABASE_URL` под локальную базу данных, например:

   ```
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/blog_db
   ```

6. Примените миграции:

   ```bash
   alembic upgrade head
   ```

7. Запустите сервер:

   ```bash
   uvicorn src.main:app --reload
   ```

Сервис будет доступен по адресу: **[http://localhost:8000](http://localhost:8000)**\
Документация API: **[http://localhost:8000/docs#](http://localhost:8000/docs#)**

---

### Вариант 2: Запуск с Docker Compose

1. Скопируйте файл `.env.example` в `.env`:

   ```bash
   cp .env.example .env
   ```

2. Соберите и запустите контейнеры:

   ```bash
   docker compose up --build
   ```

При первом запуске будут автоматически:

* подняты контейнеры приложения и базы данных,
* применены миграции Alembic,
* запущен сервер FastAPI по адресу **[http://localhost:8000](http://localhost:8000)**
* Swagger-документация доступна по ссылке **[http://localhost:8000/docs#](http://localhost:8000/docs#)**

---

## CI/CD и деплой

Проект использует **GitHub Actions** и **Render** для автоматического CI/CD.

* При пуше в любую ветку: Docker-образ автоматически собирается и публикуется в **GitHub Container Registry (GHCR)**.
* Render автоматически подтягивает последний образ из GHCR и выполняет деплой приложения и базы данных.

Последний задеплоенный билд доступен по ссылке:
🔗 **[Swagger UI — Simple Blog API (Render)](https://microservice-architecture.onrender.com/docs#)**



