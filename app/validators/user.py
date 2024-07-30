from typing import Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel

from app.models import Role

Ids = int


class NewUser(BaseModel):
    email: str
    password: str
    is_active: bool = True
    role: Role

    permissions: Optional[Union[List[Ids], None]]
    groups: Optional[Union[List[Ids], None]]
