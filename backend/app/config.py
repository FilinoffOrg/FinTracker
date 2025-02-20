import os
from dotenv import load_dotenv
from authx import AuthXConfig

load_dotenv()

# Настройки БД
DATABASE_URL = os.getenv("DATABASE_URL")

# JWT Конфигурация
config = AuthXConfig()
config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

# CORS
ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

