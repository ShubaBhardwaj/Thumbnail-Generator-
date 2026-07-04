from sqlmodel import Session, select
from fastapi import HTTPException
from src.modules.auth.model.auth_model import User
from src.common.utils.security import hash_password

def register(session: Session, name: str, email: str, password: str) -> dict:
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
    
    # Convert to dict and remove password
    user_dict = user.model_dump()
    user_dict.pop("hashed_password", None)
    
    return user_dict
