from pydantic import BaseModel
from typing import Optional, List

from model.pheart import *


# 하트가 있으면 삭제, 없으면 생성
class ManagePHeartInput(BaseModel):
    post_id: int

class ManagePHeartOutput(BaseModel):
    hasCreated: bool
    message: str
    pheart: Optional[PHeart] = None
    

# 하트 생성  
class CreatePHeartInput(BaseModel):
    post_id: int

class CreatePHeartOutput(BaseModel):
    success: int
    message: str
    pheart: Optional[PHeart] = None


# 하트 삭제
class DeletePHeartInput(BaseModel):
    post_id: str

class DeletePHeartOutput(BaseModel):
    success: int
    message: str
    pheart: Optional[List[PHeart]] = None


# 하트 조회
class HasHeartOutput(BaseModel):
    status: int
    message: str
    state: bool