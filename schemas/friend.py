from pydantic import BaseModel
from typing import Optional, Dict

from model.friend import Friend

class ManageFriendInput(BaseModel):
    friend: str

class ManageFriendOutput(BaseModel):
    hasCreated: bool
    message: str
    friend: Optional[Friend] = None


class CreateFriendInput(BaseModel):
    friend: str

class CreateFriendOutput(BaseModel):
    success: int
    message: str
    friend: Optional[Friend] = None


class DeleteFriendInput(BaseModel):
    friend: str

class DeleteFriendOutput(BaseModel):
    success: int
    message: str
    friend: Optional[list[Friend]] = None