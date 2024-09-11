from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from model.baby import *

# 아기 생성
class CreateBabyInput(BaseModel):
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


# 아기 사진
class uploadProfileImageOutput(BaseModel):
    success: bool


# 아기 정보 수정
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


# 아기 삭제
class DeleteBabyOutput(BaseModel):
    success: int

class GetBabyOutput(BaseModel):
    baby: List[Baby]