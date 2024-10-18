from pydantic import BaseModel
from typing import Optional, List

from model.pscript import *


# 스크립트가 있으면 삭제, 없으면 생성
class ManagePScriptInput(BaseModel):
    post_id: int

class ManagePScriptOutput(BaseModel):
    hasCreated: bool
    message: str
    pscript: Optional[PScript] = None


# 스크립트 생성
class CreatePScriptInput(BaseModel):
    post_id: int

class CreatePScriptOutput(BaseModel):
    success: int
    message: str
    pscript: Optional[PScript] = None


# 스크립트 삭제
class DeletePScriptInput(BaseModel):
    post_id: str

class DeletePScriptOutput(BaseModel):
    success: int
    message: str
    pscript: Optional[List[PScript]] = None


# 스크립트 조회
class HasScriptOutput(BaseModel):
    status: int
    message: str
    state: bool