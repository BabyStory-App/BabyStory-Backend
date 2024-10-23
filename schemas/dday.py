from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.dday import *

# DDay 생성
class CreateDDayInput(BaseModel):
    diary_id: int
    title: str
    content: str

class CreateDDayOutput(BaseModel):
    success: int
    message: str
    dday: Dday


# DDay 사진 추가
class UploadImageOutput(BaseModel):
    success: bool


class getdday(BaseModel):
    dday_id: int
    diary_id: int
    title: str
    post: str
    createTime: datetime
    modifyTime: Optional[datetime] = None
    hospital_id: Optional[int] = None

# DDay 가져오기
class GetDDayOutput(BaseModel):
    success: int
    message: str
    dday: List[getdday]