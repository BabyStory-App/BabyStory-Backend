from pydantic import BaseModel
from typing import Optional, List

from model.pscript import *

class CreatePScriptInput(BaseModel):
    post_id: int

class CreatePScriptOutput(BaseModel):
    success: int
    share: Optional[PScript]

class DeletePScriptInput(BaseModel):
    post_id: str

class DeletePScriptOutput(BaseModel):
    success: int
    script: Optional[PScript]