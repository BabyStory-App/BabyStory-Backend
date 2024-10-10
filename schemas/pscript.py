from pydantic import BaseModel
from typing import Optional, List

from model.pscript import *


class ManagePScriptInput(BaseModel):
    post_id: int

class ManagePScriptOutput(BaseModel):
    hasCreated: bool
    message: str
    pscript: Optional[PScript] = None


class CreatePScriptInput(BaseModel):
    post_id: int

class CreatePScriptOutput(BaseModel):
    success: int
    message: str
    pscript: Optional[PScript] = None


class DeletePScriptInput(BaseModel):
    post_id: str

class DeletePScriptOutput(BaseModel):
    success: int
    message: str
    pscript: Optional[List[PScript]] = None
