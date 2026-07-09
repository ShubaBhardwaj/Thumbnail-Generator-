from fastapi import Request, Response, status, BackgroundTasks
from sqlmodel import Session

from src.modules.auth.service import auth_service
from src.modules.auth.dto.auth_dto import UserRegisterDTO, UserLoginDTO

def register_user(session: Session, user_data: UserRegisterDTO, background_tasks: BackgroundTasks) -> dict:
    """Controller logic for registering a new user."""
    user = auth_service.register(
        session=session,
        name=user_data.name,
        email=user_data.email,
        password=user_data.password,
        background_tasks=background_tasks
    )
    return {
        "success": True,
        "message": "User registered successfully. Please check your email to verify your account.",
        "data": user
    }

async def login_user(response: Response, session: Session, user_data: UserLoginDTO) -> dict:
    """Controller logic for user login, setting secure cookies and returning user data."""
    result = auth_service.login(
        session=session,
        email=user_data.email,
        password=user_data.password
    )
    
    # Set secure HttpOnly cookies (max_age is in seconds: 7 days for refresh, 15 mins for access)
    response.set_cookie(
        key="refreshToken",
        value=result["refreshToken"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60
    )
    
    response.set_cookie(
        key="accessToken",
        value=result["accessToken"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=15 * 60
    )
    
    return {
        "success": True,
        "message": "Login Successfully",
        "data": {
            "user": result["user"],
            "accessToken": result["accessToken"]
        }
    }

async def logout_user(request: Request, response: Response, session: Session) -> dict:
    """Controller logic for user logout, clearing cookies and deleting the active refresh token."""
    refresh_token = request.cookies.get("refreshToken")
    
    if refresh_token:
        # Clear token in database
        auth_service.logout(session=session, refresh_token=refresh_token)
        
    # Clear both cookies on the client side
    response.delete_cookie(
        key="refreshToken",
        httponly=True,
        secure=True,
        samesite="lax"
    )
    response.delete_cookie(
        key="accessToken",
        httponly=True,
        secure=True,
        samesite="lax"
    )
    
    return {
        "success": True,
        "message": "Logged out successfully"
    }

def verify_user(session: Session, token: str) -> dict:
    """Controller logic for verifying user email."""
    return auth_service.verify_user(session=session, token=token)

