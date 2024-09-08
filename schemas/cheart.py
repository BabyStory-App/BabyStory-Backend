from pydantic import BaseModel
from typing import Optional, List

from model.cheart import *

class CreateCHeartInput(BaseModel):
    comment_id: int

class CreateCHeartOutput(BaseModel):
    success: int
    cheart: Optional[CHeart]

class DeleteCHeartInput(BaseModel):
    comment_id: int

class DeleteCHeartOutput(BaseModel):
    success: int
    cheart: Optional[CHeart]