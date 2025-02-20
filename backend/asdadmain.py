from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.future import select
from sqlalchemy import MetaData
from passlib.context import CryptContext
from typing import Annotated

import os
import asyncio

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# AuthX конфигурация
config = AuthXConfig()
config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=config)

# Настройки БД
engine = create_async_engine(os.getenv("DATABASE_URL"))
new_session = async_sessionmaker(engine, expire_on_commit=False)

# CORS
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Зависимость для получения сессии
async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

# БД модели
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

class UserLoginSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserCreateSchema(UserLoginSchema):
    pass

# Инициализация БД
async def setup_database():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Регистрация
@app.post("/register")
async def register(user: UserCreateSchema, response: Response, session: SessionDep):
    result = await session.execute(select(User).where(User.username == user.username))
    user_in_db = result.scalar_one_or_none()

    if user_in_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, password_hash=hashed_password)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    token = security.create_access_token(uid=new_user.username)
    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=True,
        samesite="Lax"
    )

    return {"access_token": token}

# Логин
@app.post("/login")
async def login(credentials: UserLoginSchema, response: Response, session: SessionDep):
    result = await session.execute(select(User).where(User.username == credentials.username))
    user = result.scalar_one_or_none()

    if not user or not pwd_context.verify(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = security.create_access_token(uid=user.id)
    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=True,
        samesite="Lax"
    )

    return {"access_token": token}

# Защищённый маршрут
@app.get("/protected")
async def protected(user=Depends(security.access_token_required)):
    return {"data": "This is a protected route", "user": user}

# Запуск сервера
if __name__ == "__main__":
    asyncio.run(setup_database())  # Создаёт таблицы при старте
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

