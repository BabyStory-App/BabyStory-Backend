from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from model.baby import *

class CreateBabyInput(BaseModel):
    baby_id: str
    obn: str
    name: Optional[str]
    gender: Optional[int]
    birthDate: Optional[datetime]
    bloodType: Optional[str]
    cm: Optional[float]
    kg: Optional[float]
    photoId: Optional[str]

class CreateBabyOutput(BaseModel):
    baby: Optional[Baby]
    
class UpdateBabyInput(BaseModel):
    baby_id: str
    obn: str
    name: Optional[str]
    gender: Optional[int]
    birthDate: Optional[datetime]
    bloodType: Optional[str]
    cm: Optional[float]
    kg: Optional[float]
    photoId: Optional[str]

class UpdateBabyOutput(BaseModel):
    success: int
    baby: Optional[Baby]

class DeleteBabyOutput(BaseModel):
    success: int

class GetBabyOutput(BaseModel):
    baby: List[Baby]