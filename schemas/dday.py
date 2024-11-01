from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.dday import *

class day(BaseModel):
    dday_id: int
    diary_id: int
    title: str
    content: str
    createTime: datetime
    modifyTime: Optional[datetime] = None
    add: Optional[dict] = None

# DDay 생성
class CreateDDayInput(BaseModel):
    diary_id: int
    createTime: str
    title: str
    content: str

class CreateDDayOutput(BaseModel):
    success: int
    message: str
    dday: Dday


# DDay 사진 업로드
class PhotoUploadOutput(BaseModel):
    success: int
    message: str


class getdday(BaseModel):
    dday_id: int
    diary_id: int
    title: str
    content: str
    photoId: Optional[List[str]]
    createTime: datetime
    modifyTime: Optional[datetime] = None
    add: Optional[dict] = None

class allday(BaseModel):
    dday_id: int
    title: str
    createTime: datetime

# 산모수첩에 대한 전체 DDay 조회
class GetAllDDayOutput(BaseModel):
    success: int
    message: str
    dday: List[allday]

# DDay 가져오기
class GetDDayOutput(BaseModel):
    success: int
    message: str
    dday: List[getdday]


# DDay 수정
class UpdateDDayInput(BaseModel):
    dday_id: int
    title: str
    content: str

class UpdateDDayOutput(BaseModel):
    success: int
    message: str
    dday: day


# DDay 사진 추가
class PhotoUpdateOutput(BaseModel):
    success: int
    message: str


# DDay 삭제
class DeleteDDayOutput(BaseModel):
    success: int
    message: str