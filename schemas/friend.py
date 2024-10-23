from pydantic import BaseModel
from typing import Optional, Dict

from model.friend import Friend

# 친구관계 관리
class ManageFriendInput(BaseModel):
    friend: str

class ManageFriendOutput(BaseModel):
    hasCreated: bool
    message: str
    friend: Optional[Friend] = None


# 친구관계 생성
class CreateFriendInput(BaseModel):
    friend: str

class CreateFriendOutput(BaseModel):
    success: int
    message: str
    friend: Optional[Friend] = None


# 친구관계 삭제
class DeleteFriendInput(BaseModel):
    friend: str

class DeleteFriendOutput(BaseModel):
    success: int
    message: str
    friend: Optional[list[Friend]] = None