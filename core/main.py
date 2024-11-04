from fastapi import FastAPI
from api.index import app_router
from fastapi.responses import JSONResponse 
from config.middlewares.index import appMiddleware
app = FastAPI()
app.add_middleware(appMiddleware)

    
@app.get("/")
async def main():
    return { "status_code" : 200 }
    

app.include_router(router=app_router, prefix="/api")
