from typing import Annotated

from annotated_types import MinLen, MaxLen

from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict,
)


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(5), MaxLen(50)]
    email: EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
