from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class User(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    phone: str = Field(default='')


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
