from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.baby import *

# 아기 생성
class CreateBabyInput(BaseModel):
    baby_id: str
    obn: str
    name: str
    gender: int
    birthDate: datetime
    bloodType: str
    cm: float
    kg: float
    photoId: Optional[str]


class CreateBabyOutput(BaseModel):
    baby: Optional[Baby]
    

# 아기 정보 수정

class UpdateBabyInput(BaseModel):
    baby_id: str
    obn: str
    name: str
    gender: int
    birthDate: datetime
    bloodType: str
    cm: float
    kg: float
    photoId: Optional[str]


class UpdateBabyOutput(BaseModel):
    success: int
    baby: Optional[Baby]

# 아기 삭제

class DeleteBabyOutput(BaseModel):
    success: int

# 아기 정보 가져오기
class GetBabyOutput(BaseModel):
    baby: List[Baby]


