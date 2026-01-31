from pydantic import BaseModel
from datetime import datetime

class PacientReadSchema(BaseModel):
    id: int
    fio: str 
    date_birth: int
    status: bool 
    location_clinic: str
    date_start: datetime 
    date_end: datetime 


class PacientCreateSchema(BaseModel):
    fio: str 
    date_birth: int
    status: bool 
    location_clinic: str 
    date_start: datetime 
    date_end: datetime 


class PacientUpdateSchema(BaseModel):
    fio: str 
    date_birth: int
    status: bool 
    location_clinic: str 
    date_start: datetime 
    date_end: datetime 

    
