from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.common.config.database import get_session
from src.modules.auth.service.auth_service import register
from src.modules.auth.dto.auth_dto import UserRegister

router = APIRouter()


@router.post("/auth/register")
async def register_user(user_data: UserRegister, session: Session = Depends(get_session)):
    return register(
        session=session,
        name=user_data.name,
        email=user_data.email,
        password=user_data.password
    )