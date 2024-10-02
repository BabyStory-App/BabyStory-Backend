from pydantic import BaseModel
from typing import Optional, List

from model.pheart import *


class ManagePHeartInput(BaseModel):
    post_id: int
    
    
class CreatePHeartInput(BaseModel):
    post_id: int

class CreatePHeartOutput(BaseModel):
    success: int
    pheart: Optional[PHeart] = None


class DeletePHeartInput(BaseModel):
    post_id: str


class DeletePHeartOutput(BaseModel):
    success: int
    pheart: Optional[PHeart] = None
