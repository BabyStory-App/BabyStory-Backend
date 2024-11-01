from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.diary import *

# 다이어리 생성
class CreateDiaryInput(BaseModel):
    baby_id: str
    born: int
    title: str

class CreateDiaryOutput(BaseModel):
    success: int
    message: str
    diary: Optional[Diary] = None


# 다이어리 표지 사진 업로드
class UploadDiaryCoverOutput(BaseModel):
    success: int
    message: str


class GDiary(BaseModel):
    diary_id: int
    parent_id: str
    baby_id: str
    born: int
    title: str
    createTime: datetime
    modifyTime: Optional[datetime] = None
    cover: Optional[str] = None


# 아기의 모든 다이어리 가져오기
class GetDiaryOutput(BaseModel):
    success: int
    message: str
    diary: Optional[GDiary] = None


# 하나의 다이어리 가져오기
class GetDiaryOutput(BaseModel):
    success: int
    message: str
    diary: Optional[List[GDiary]] = None


# 다이어리 수정
class UpdateDiaryInput(BaseModel):
    diary_id: int
    title: str

class UpdateDiaryOutput(BaseModel):
    success: int
    message: str
    diary: Optional[Diary] = None


# 다이어리 표지 사진 수정
class UpdateDiaryCoverOutput(BaseModel):
    success: int
    message: str


# 다이어리 삭제
class DeleteDiaryOutput(BaseModel):
    success: int
    message: str