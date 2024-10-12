from pydantic import BaseModel
from typing import Optional, List

from model.cheart import *


class ManageCHeartInput(BaseModel):
    comment_id: int

class ManageCHeartOutput(BaseModel):
    hasCreated: bool
    message: str
    cheart: Optional[CHeart] = None


class CreateCHeartInput(BaseModel):
    comment_id: int

class CreateCHeartOutput(BaseModel):
    success: int
    message: str
    cheart: Optional[CHeart] = None


class DeleteCHeartInput(BaseModel):
    comment_id: int

class DeleteCHeartOutput(BaseModel):
    success: int
    message: str
    cheart: Optional[CHeart] = None
