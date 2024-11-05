from pydantic import BaseModel
from typing import List


class JwtToken(BaseModel):
    permissions: List[str]
    exp: int
    iat: int
