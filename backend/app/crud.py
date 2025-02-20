from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas import UserCreateSchema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Получение пользователя по username
async def get_user_by_username(session: AsyncSession, username: str):
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


# Создание нового пользователя
async def create_user(session: AsyncSession, user: UserCreateSchema):
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, password_hash=hashed_password)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user

