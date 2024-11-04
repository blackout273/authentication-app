from fastapi import APIRouter, Security
from ..schemas.index import router_sso

controller_router_v1 = APIRouter()
@controller_router_v1.get("/")
async def main():
    return { "message api":"control ok"}

controller_router_v1.include_router(router=router_sso,prefix="/sso")