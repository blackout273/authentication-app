from fastapi import Request, HTTPException
from dotenv import dotenv_values
from typing import List
from ..models.model_token import JwtToken
import jwt, json


config = dotenv_values(f".env.{dotenv_values('.env').get('PYTHON_ENV')}")


class AuthPermissions:
    def __init__(self, perms: List[str]):
        self.perms = perms

    async def __call__(self, req: Request):
        self.req = req
        print("OTHERSIDE",self.req.state.permissions)
        headers: str = req.headers.get("authorization", None)
        authorization: str = headers.replace("Bearer ", "")
        result: JwtToken = await self.verifyJwt(authorization)

        if not result:
            raise HTTPException(status_code=401, detail="AUTHENTICATION ERROR")

        for permission in self.req.state.permissions: #json.loads(result.get("permissions","[]")):
            if permission in self.perms:
                return True
        raise HTTPException(status_code=401, detail="VOCE NÃO POSSUI PERMISSÃO PARA ACESSAR O RECURSO")

    async def verifyJwt(self, value):
        return jwt.decode(jwt=value, key=config.get("SECRET_JWT"), algorithms=["RS256"])
