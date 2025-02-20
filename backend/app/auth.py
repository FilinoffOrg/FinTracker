from fastapi import HTTPException, Response, Depends
from sqlalchemy.orm import Session
from app.crud import get_user_by_username, create_user
from app.schemas import UserCreateSchema, UserLoginSchema
from app.config import config
from authx import AuthX
from passlib.context import CryptContext
from app.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

security = AuthX(config=config)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register(user, response, session: AsyncSession = Depends(get_session)):
    if await get_user_by_username(session, user.username):
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = await create_user(session, user)
    token = security.create_access_token(uid=new_user.username)

    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=True,
        samesite="Lax"
    )

    return {"access_token": token}


async def login(credentials: UserLoginSchema, response: Response, session: Session = Depends(get_session)):
    user = await get_user_by_username(session, credentials.username)

    if not user or not pwd_context.verify(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = security.create_access_token(uid=str(user.id))

    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=True,
        samesite="Lax"
    )

    return {"access_token": token}

