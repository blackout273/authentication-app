from fastapi import FastAPI
from api.index import app_router
from fastapi.responses import JSONResponse 
from config.middlewares.index import appMiddleware
from dotenv import dotenv_values
from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool

config = dotenv_values(f".env.{dotenv_values('.env').get('PYTHON_ENV')}")

def get_conn_str():
    return f"""
    dbname={config.get('POSTGRES_DB')}
    user={config.get('POSTGRES_USER')}
    password={config.get('POSTGRES_PASSWORD')}
    host={config.get('POSTGRES_HOST')}
    port={config.get('POSTGRES_PORT')}
    """

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.async_pool = AsyncConnectionPool(conninfo=get_conn_str(), open=False)
    await app.async_pool.open()
    yield
    await app.async_pool.close()

app = FastAPI(lifespan=lifespan)
app.add_middleware(appMiddleware)

    
@app.get("/")
async def main():
    return { "status_code" : 200 }
    

app.include_router(router=app_router, prefix="/api")
