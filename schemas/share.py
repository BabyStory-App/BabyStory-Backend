from pydantic import BaseModel
from typing import Optional, List

from model.share import *

class CreateShareInput(BaseModel):
    post_id: int
    parent_id: str

class CreateShareOutput(BaseModel):
    success: int
    share: Optional[Share]

class DeleteShareInput(BaseModel):
    post_id: int
    parent_id: str

class DeleteShareOutput(BaseModel):
    success: int
    share: Optional[Share]