# Amo-test-task

## Система мониторинга серверов

Django приложение для сбора метрик с удаленных серверов и создания инцидентов

### Технологический стек

- ***Backend:*** Django 5.0
- ***Database:*** MySQL 8.0
- ***Task Queue:*** Celery + Redis

### Установка и запуск

#### Требования

- Python 3.12
- MySQL 8.0+
- Docker compose

#### 1. Настройка окружения 

Создайте .env файл по шаблону - .env.axample

#### 2. Установка зависимостей

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Запуск Redis из Docker

`docker compose up -d`

#### 4. Запуск приложения

`python manage.py runserver`