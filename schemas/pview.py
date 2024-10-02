from pydantic import BaseModel
from typing import Optional, List

from model.pview import *


class ManagePViewInput(BaseModel):
    post_id: int

class CreatePViewInput(BaseModel):
    post_id: int


class CreatePViewOutput(BaseModel):
    success: int
    pview: Optional[PView] = None


class DeletePViewInput(BaseModel):
    post_id: str


class DeletePViewOutput(BaseModel):
    success: int
    pview: Optional[PView] = None
