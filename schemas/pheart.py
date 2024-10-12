from pydantic import BaseModel
from typing import Optional, List

from model.pheart import *


class ManagePHeartInput(BaseModel):
    post_id: int

class ManagePHeartOutput(BaseModel):
    hasCreated: bool
    message: str
    pheart: Optional[PHeart] = None
    
    
class CreatePHeartInput(BaseModel):
    post_id: int

class CreatePHeartOutput(BaseModel):
    success: int
    message: str
    pheart: Optional[PHeart] = None


class DeletePHeartInput(BaseModel):
    post_id: str

class DeletePHeartOutput(BaseModel):
    success: int
    message: str
    pheart: Optional[List[PHeart]] = None
