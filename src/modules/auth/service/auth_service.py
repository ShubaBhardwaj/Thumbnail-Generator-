import hashlib
from sqlmodel import Session, select
from fastapi import HTTPException, status, BackgroundTasks
from src.modules.auth.model.auth_model import User
from src.common.utils.security import hash_password, verify_password
from src.common.utils.jwt import (
    generateAccessToken,
    generateRefreshToken,
    generate_verification_token,
    verify_verification_token,
)
from src.common.config.env_config import APP_URL
from src.common.utils.email import send_verification_email

def hash_token(token: str) -> str:
    """Hash a token using SHA-256."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def register(session: Session, name: str, email: str, password: str, background_tasks: BackgroundTasks) -> dict:
    # Check if user already exists
    statement = select(User).where(User.email == email)
    is_exist = session.exec(statement).first()
    if is_exist:
        raise HTTPException(status_code=409, detail="Email already exist")
    
    # Hash the password
    hashed_pwd = hash_password(password)
    
    # Create the user object
    user = User(
        username=name,
        email=email,
        hashed_password=hashed_pwd,
        is_active=True,
        is_verified=False
    )
    
    # Persist the user
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Generate verification token
    token_payload = {"email": email, "id": user.id}
    verification_token = generate_verification_token(token_payload)
    
    # Build verification URL
    verification_url = f"{APP_URL}/auth/verify?token={verification_token}"
    
    # Enqueue verification email sending
    background_tasks.add_task(
        send_verification_email,
        email=email,
        username=name,
        verification_url=verification_url
    )
    
    # Convert to dict and remove password
    user_dict = user.model_dump()
    user_dict.pop("hashed_password", None)
    user_dict.pop("refresh_token", None)
    
    return user_dict

def login(session: Session, email: str, password: str) -> dict:
    """Login a user, verify password/status, and generate access/refresh tokens."""
    # 1. Find user by email
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user not found"
        )
        
    # 2. Check user verification status
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user not verified"
        )
        
    # 3. Check the password
    is_match = verify_password(password, user.hashed_password)
    if not is_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
        
    # 4. Generate tokens
    access_token = generateAccessToken({"id": user.id, "role": user.role})
    refresh_token = generateRefreshToken({"id": user.id})
    
    # 5. Hash refresh token and save
    hashed_refresh = hash_token(refresh_token)
    user.refresh_token = hashed_refresh
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # 6. Prepare user object response
    user_dict = user.model_dump()
    user_dict.pop("hashed_password", None)
    user_dict.pop("refresh_token", None)
    
    return {
        "user": user_dict,
        "accessToken": access_token,
        "refreshToken": refresh_token
    }

def logout(session: Session, refresh_token: str) -> bool:
    """Clear refresh token from the database for the user associated with this refresh token."""
    hashed_refresh = hash_token(refresh_token)
    statement = select(User).where(User.refresh_token == hashed_refresh)
    user = session.exec(statement).first()
    if user:
        user.refresh_token = None
        session.add(user)
        session.commit()
        return True
    return False

def verify_user(session: Session, token: str) -> dict:
    """Verify a user's email using the verification token."""
    payload = verify_verification_token(token)
    email = payload.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token payload"
        )
        
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    if user.is_verified:
        return {
            "success": True,
            "message": "User is already verified"
        }
        
    user.is_verified = True
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {
        "success": True,
        "message": "Email verified successfully"
    }


