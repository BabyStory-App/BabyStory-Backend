from pydantic import BaseModel
from typing import Optional, List

from model.pview import *


class ManagePViewInput(BaseModel):
    post_id: int

class ManagePViewOutput(BaseModel):
    hasCreated: bool
    message: str
    pview: Optional[PView] = None


class CreatePViewInput(BaseModel):
    post_id: int

class CreatePViewOutput(BaseModel):
    success: int
    message: str
    pview: Optional[PView] = None


class DeletePViewInput(BaseModel):
    post_id: str

class DeletePViewOutput(BaseModel):
    success: int
    message: str
    pview: Optional[List[PView]] = None
