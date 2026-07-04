from datetime import datetime, timezone
from typing import Optional, List
from uuid import uuid4
from sqlmodel import SQLModel, Field, Relationship

def generate_uuid() -> str:
    return str(uuid4())

def get_current_utc_time() -> datetime:
    return datetime.now(timezone.utc)

class User(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    created_at: datetime = Field(default_factory=get_current_utc_time)
    updated_at: datetime = Field(default_factory=get_current_utc_time)