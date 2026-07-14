from fastapi import APIRouter, Depends, Request, Response, BackgroundTasks
from sqlmodel import Session
from src.common.config.database import get_session
from src.modules.auth.controller import auth_controller
from src.modules.auth.dto.auth_dto import UserRegisterDTO, UserLoginDTO

router = APIRouter()

@router.post("/auth/register")
async def register(
    user_data: UserRegisterDTO,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    """Endpoint for user registration, delegating to the controller."""
    return auth_controller.register_user(
        session=session,
        user_data=user_data,
        background_tasks=background_tasks
    )

@router.get("/auth/verify")
async def verify(token: str, session: Session = Depends(get_session)):
    """Endpoint to verify user email using the token sent in registration email."""
    return auth_controller.verify_user(session=session, token=token)

@router.post("/auth/login")
async def login(response: Response, user_data: UserLoginDTO, session: Session = Depends(get_session)):
    """Endpoint for user login, delegating to the controller."""
    return await auth_controller.login_user(response=response, session=session, user_data=user_data)

@router.post("/auth/logout")
async def logout(request: Request, response: Response, session: Session = Depends(get_session)):
    """Endpoint for user logout, delegating to the controller."""
    return await auth_controller.logout_user(request=request, response=response, session=session)

@router.post("/auth/refresh")
async def refresh(request: Request, response: Response, session: Session = Depends(get_session)):
    """Endpoint to refresh access and refresh tokens using the stored refresh token."""
    return await auth_controller.refresh_tokens(request=request, response=response, session=session)