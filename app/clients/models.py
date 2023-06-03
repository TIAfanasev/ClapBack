from typing import Any

from pydantic import BaseModel


class Session(BaseModel):
    session: Any # should have been AsyncSession but OpenAPI can't show this type.


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    user_id: int
