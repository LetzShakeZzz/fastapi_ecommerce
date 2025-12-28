# fastapi_ecommerce

Краткие инструкции для запуска проекта локально.

1. Создайте и активируйте виртуальное окружение (из корня проекта):

```sh
python -m venv .venv
source .venv/bin/activate
```

2. Установите зависимости:

```sh
pip install -r requirements.txt
```

3. Создайте файл `.env` в корне проекта с переменными окружения (пример):

```
# JWT
SECRET_KEY=...

# Postgres
PG_HOST=...
PG_PORT=...
PG_USER=...
PG_PASS=...
PG_NAME=...
```


4. Примените миграции, чтобы создать схему:

```sh
# из корня проекта
alembic upgrade head
```

5. Запустите сервер разработки:

```sh
uvicorn app.main:app --reload
```