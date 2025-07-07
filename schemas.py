from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Temptest(BaseModel):
    tempreg : str
    status : str


class TemptestRead(Temptest):
    id : int
    created_at : datetime
    updated_at : datetime


class TemptestPatch(BaseModel):
    tempreg: Optional[str] = None
    status: Optional[str] = None


class TemptestDelete(BaseModel):
   id : int
