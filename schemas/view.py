from pydantic import BaseModel
from typing import Optional, List

from model.view import *

class CreateViewInput(BaseModel):
    post_id: int
    parent_id: str

class CreateViewOutput(BaseModel):
    success: int
    view: Optional[View]

class DeleteViewInput(BaseModel):
    post_id: int
    parent_id: str

class DeleteViewOutput(BaseModel):
    success: int
    view: Optional[View]