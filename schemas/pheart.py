from pydantic import BaseModel
from typing import Optional, List

from model.pheart import *

class CreatePHeartInput(BaseModel):
    post_id: int

class CreatePHeartOutput(BaseModel):
    success: int
    pheart: Optional[PHeart]

class DeletePHeartInput(BaseModel):
    post_id: str

class DeletePHeartOutput(BaseModel):
    success: int
    pheart: Optional[PHeart]