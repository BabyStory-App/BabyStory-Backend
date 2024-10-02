from pydantic import BaseModel
from typing import Optional, List

from model.cheart import *


class ManageCHeartInput(BaseModel):
    comment_id: int


class CreateCHeartInput(BaseModel):
    comment_id: int

class CreateCHeartOutput(BaseModel):
    success: int
    cheart: Optional[CHeart] = None


class DeleteCHeartInput(BaseModel):
    comment_id: int

class DeleteCHeartOutput(BaseModel):
    success: int
    cheart: Optional[CHeart] = None
