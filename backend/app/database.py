from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)

# Базовый класс для моделей
class Base(DeclarativeBase):
    pass

# Получение сессии БД
async def get_session() -> AsyncSession:
    async with new_session() as session:
        yield session

