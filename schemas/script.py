from pydantic import BaseModel
from typing import Optional, List

from model.pscript import *

class CreateScriptInput(BaseModel):
    post_id: int
    parent_id: str

class CreateScriptOutput(BaseModel):
    success: int
    share: Optional[Script]

class DeleteScriptInput(BaseModel):
    post_id: int
    parent_id: str

class DeleteScriptOutput(BaseModel):
    success: int
    script: Optional[Script]