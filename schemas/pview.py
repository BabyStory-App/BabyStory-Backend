from pydantic import BaseModel
from typing import Optional, List

from model.pview import *


# 포스트 조회
class ManagePViewInput(BaseModel):
    post_id: int

class ManagePViewOutput(BaseModel):
    hasCreated: bool
    message: str
    pview: Optional[PView] = None


# 포스트 조회 생성
class CreatePViewInput(BaseModel):
    post_id: int

class CreatePViewOutput(BaseModel):
    success: int
    message: str
    pview: Optional[PView] = None


# 포스트 조회 삭제
class DeletePViewInput(BaseModel):
    post_id: str

class DeletePViewOutput(BaseModel):
    success: int
    message: str
    pview: Optional[List[PView]] = None
