from pydantic import BaseModel
from typing import Optional

class sessionData(BaseModel):
    isValid: bool
    
class meData(BaseModel):
    name: str
    mail: str
    
class dataObjects(BaseModel):
    me: Optional[meData]
    session: Optional[sessionData]
    
class Response(BaseModel):
    status: int 
    message: str
    metaData: Optional[dataObjects] = None