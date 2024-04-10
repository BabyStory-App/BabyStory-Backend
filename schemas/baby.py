from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from model.baby import *

# 아기 생성
class create_baby_input(BaseModel):
    baby_id: str
    name: str
    gender: str
    birthDate: datetime
    bloodType: str
    photoId: Optional[str]

class create_baby_output(BaseModel):
    success: int
    baby: Optional[Baby]

# 아기 정보 수정
class update_baby_input(BaseModel):
    baby_id: str
    name: Optional[str]
    gender: Optional[str]
    birthDate: Optional[datetime]
    bloodType: Optional[str]
    photoId: Optional[str]

class update_baby_output(BaseModel):
    success: int
    baby: Optional[Baby]

# 아기 삭제
class delete_baby_input(BaseModel):
    baby_id: str

class delete_baby_output(BaseModel):
    success: int
    baby_id: Optional[str]