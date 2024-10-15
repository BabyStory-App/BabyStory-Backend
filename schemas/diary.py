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
    success: bool
    message: str