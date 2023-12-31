from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str = Field(default='')
    is_admin: bool


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
