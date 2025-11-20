# MiniAPI

MiniAPI — це простий Django-проєкт для завантаження CSV-файлів та обробки їх асинхронно за допомогою Celery.

## Технології
- Python 3.12
- Django 5.2
- PostgreSQL 17.4
- Redis 7.4
- Celery
- Docker & Docker Compose
- Flower

## Установка та запуск

1. Клонування репозиторію
```bash
git clone https://github.com/PySlava/miniapicsv
```

2. Створення .env файлу (для змінних середовища)
```bash
POSTGRES_DB=recordcsv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
3. Запуск Docker-контейнерів
```bash
docker compose up --build
```

4. Міграції бази даних
```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

5. Підключення до БД
```bash
docker compose exec db psql -U postgres -d recordcsv
```

6. Створення суперкористувача (для адмінки)
```bash
docker compose exec web python manage.py createsuperuser
```

7. Веб-сервер доступний за адресою
```bash
http://localhost:8000/
```

## Завантаження CSV
1. Перейти на сторінку http://localhost:8000/upload/.
2. Завантажити CSV-файл у форматі (я його окремо додав в проєкт під назвою example.csv, де 2 даних коректні, а 3 даних є не коректні):

- name,email,age
- Slava Polivoda,slava.polivoda@gmail.com,28
- Robota Uaa,robota.ua@gmail.com,34

**Celery обробляє файл асинхронно**

Результат можна перевірити у базі даних або через адмінку http://localhost:8000/admin/.

## Запуск Celery та Flower

- Celery worker
```bash
docker compose exec web celery -A baseapi worker --loglevel=info
```

- Flower (моніторинг Celery)
```bash
docker compose exec web celery -A baseapi flower
```
Після чого можна відкрити в браузері Flower для моніторингу таски і продивитись всі логи:
```bash
http://localhost:5555/
```