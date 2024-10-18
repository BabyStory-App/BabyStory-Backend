from pydantic import BaseModel
from typing import Optional, List

from model.cheart import *


# 하트가 있으면 삭제, 없으면 생성
class ManageCHeartInput(BaseModel):
    comment_id: int

class ManageCHeartOutput(BaseModel):
    hasCreated: bool
    message: str
    cheart: Optional[CHeart] = None


# 하트 생성
class CreateCHeartInput(BaseModel):
    comment_id: int

class CreateCHeartOutput(BaseModel):
    success: int
    message: str
    cheart: Optional[CHeart] = None


# 하트 삭제
class DeleteCHeartInput(BaseModel):
    comment_id: int

class DeleteCHeartOutput(BaseModel):
    success: int
    message: str
    cheart: Optional[CHeart] = None


# 하트 조회
class HasHeartOutput(BaseModel):
    status: int
    message: str
    state: bool