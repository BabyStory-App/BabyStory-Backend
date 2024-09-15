from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from model.baby import *

# 아기 생성


class CreateBabyInput(BaseModel):
    obn: str
    name: Optional[str] = None
    gender: Optional[int] = None
    birthDate: Optional[datetime] = None
    bloodType: Optional[str] = None
    cm: Optional[float] = None
    kg: Optional[float] = None
    photoId: Optional[str] = None


class CreateBabyOutput(BaseModel):
    baby: Optional[Baby] = None


# 아기 사진
class uploadProfileImageOutput(BaseModel):
    success: int


# 아기 정보 수정
class UpdateBabyInput(BaseModel):
    baby_id: str
    obn: str
    name: Optional[str] = None
    gender: Optional[int] = None
    birthDate: Optional[datetime] = None
    bloodType: Optional[str] = None
    cm: Optional[float] = None
    kg: Optional[float] = None
    photoId: Optional[str] = None


class UpdateBabyOutput(BaseModel):
    success: int
    baby: Optional[Baby] = None


# 아기 삭제
class DeleteBabyOutput(BaseModel):
    success: int


class GetBabyOutput(BaseModel):
    baby: List[Baby]
