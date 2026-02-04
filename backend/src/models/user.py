from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy import String

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)

class User(UserBase, table=True):
    """
    User model representing an authenticated user of the system.
    Managed through Better Auth as specified in the requirements.
    """
    id: Optional[str] = Field(sa_type=String, default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str = Field(nullable=False)  # Managed by Better Auth
    is_active: bool = Field(default=True)  # User is active by default
    first_name: Optional[str] = Field(default=None, max_length=100)  # Optional first name
    last_name: Optional[str] = Field(default=None, max_length=100)   # Optional last name
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)