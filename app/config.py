import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# PostgreSQL settings
PG_HOST=os.getenv("PG_HOST")
PG_PORT=os.getenv("PG_PORT")
PG_USER=os.getenv("PG_USER")
PG_PASS=os.getenv("PG_PASS")
PG_NAME=os.getenv("PG_NAME")
# Строка подключения для PostgreSQl
PG_DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_NAME}"