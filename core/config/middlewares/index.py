from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request , HTTPException
from fastapi.responses import JSONResponse
import jwt, json
from dotenv import dotenv_values
config = dotenv_values(f".env.{dotenv_values('.env').get('PYTHON_ENV')}")

class appMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
        headers = request.headers.get('authorization', None)
        has_error=""
        try:
            if not headers:
                raise HTTPException(status_code=401, detail="AUTHENTICATION ERROR")
            if "Bearer" not in headers:
                raise HTTPException(status_code=401, detail="INVALID TOKEN")
            authorization = headers.replace("Bearer ","")
            await self.verifyJwt(authorization)
            
        except Exception as ex:
            has_error = ex   
        finally:
            if(has_error):
                return JSONResponse(status_code=has_error.status_code, content={'message':has_error.detail})  
            
            response = await call_next(request)
            return response 
        
    async def verifyJwt(self,value):
        try:
            jwt_decoded = jwt.decode(jwt=value, key=config.get('SECRET_JWT'),options={"verify_exp": True}, algorithms=['RS256'])
            print(jwt_decoded)
        except Exception as ex:
            raise HTTPException(status_code=401, detail="InvalidSignatureError")
