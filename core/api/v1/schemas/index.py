from fastapi import APIRouter
from .me.index import router_me
router_sso = APIRouter()

@router_sso.get("/")
async def main():
    return { "message api":"SSO ok"}

router_sso.include_router(router=router_me,prefix="/me")