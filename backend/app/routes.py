from fastapi import APIRouter, Depends
from app.auth import register, login, security
from app.schemas import UserCreateSchema, UserLoginSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import Response
from app.database import get_session
router = APIRouter()

@router.post("/register")
async def register_user(
    user: UserCreateSchema,
    response: Response,
    session: AsyncSession = Depends(get_session)  # Добавлено внедрение сессии
):
    return await register(user, response, session)  # Передаем сессию


@router.post("/login")
async def login_user(
    credentials: UserLoginSchema,
    response: Response,
    session: AsyncSession = Depends(get_session)  # Добавлено внедрение сессии
):
    return await login(credentials, response, session)  # Передаем сессию

@router.get("/protected")
async def protected_route(user=Depends(security.access_token_required)):
    return {"data": "This is a protected route", "user": user}

