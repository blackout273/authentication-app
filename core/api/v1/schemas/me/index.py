from fastapi import APIRouter
router_me = APIRouter()

@router_me.get("/")
async def main():
    return { "message":"me ok"}