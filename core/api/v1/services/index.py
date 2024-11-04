from fastapi import Request , HTTPException
import jwt
from dotenv import dotenv_values
config = dotenv_values(f".env.{dotenv_values('.env').get('PYTHON_ENV')}")

class VerifyRequest:
    def __init__(self):
        # print(config.get('SECRET_JWT'))
        pass
    def __call__(self, req: Request):
        self.req = req
        headers = req.headers.get('authorization', None)
        if not headers:
            raise HTTPException(status_code=401, detail="AUTHENTICATION ERROR")
        
        if "Bearer" not in headers:
            raise HTTPException(status_code=401, detail="INVALID TOKEN")
            
        authorization = headers.replace("Bearer ","")
        self.verifyJwt(authorization)
        
            
            
    
    def verifyJwt(self,value):
        jwt_decoded = jwt.decode(jwt=value, key=config.get('SECRET_JWT'), algorithms=['RS256'])
        
    