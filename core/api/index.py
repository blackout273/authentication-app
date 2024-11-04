from fastapi import APIRouter
from .v1.controllers.index import controller_router_v1
app_router = APIRouter()

@app_router.get("/")
async def main():
    return { "message api":"control ok"}

app_router.include_router(router=controller_router_v1,prefix="/v1")