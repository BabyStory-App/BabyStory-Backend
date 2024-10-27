from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.milk import *

# 수유일지 생성
class CreateMilkInput(BaseModel):
    diary_id: int
    baby_id: str
    milk: int
    amount: int
    mtime: datetime

class CreateMilkOutput(BaseModel):
    success: int
    message: str
    milk: Milk


# 해당 날짜의 수유일지 조회
class GetMilkOutput(BaseModel):
    success: int
    message: str
    milks: Milk


# 다이어리에 대한 전체 수유일지 조회
class GetMilkInput(BaseModel):
    diary_id: int
    start_time: datetime
    end_time: datetime

class GetMilkOutput(BaseModel):
    success: int
    message: str
    milks: List[Milk]


# 수유일지 수정
class UpdateMilkInput(BaseModel):
    milk_id: int
    milk: int
    amount: int
    mtime: datetime

class UpdateMilkOutput(BaseModel):
    success: int
    message: str
    milk: Milk


# 수유일지 삭제
class DeleteMilkOutput(BaseModel):
    success: bool
    message: str