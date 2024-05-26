from pydantic import BaseModel
from typing import Optional, Dict

from model.parent import Parent


class CreateParentInput(BaseModel):
    parent_id: str
    password: str
    email: str
    name: str
    nickname: str
    signInMethod: str
    emailVerified: bool
    photoId: Optional[str]
    description: Optional[str]
    mainaddr: Optional[str]
    subaddr: Optional[str]


class CreateParentOutput(BaseModel):
    parent: Optional[Parent]
    x_jwt: str


class GetParentByEmailOutput(BaseModel):
    parent: Optional[Parent]
    x_jwt: str


class UpdateParentInput(BaseModel):
    password: str
    email: str
    name: str
    nickname: str
    signInMethod: str
    emailVerified: bool
    photoId: Optional[str]
    description: Optional[str]
    mainaddr: Optional[str]
    subaddr: Optional[str]

class UpdateParentOutput(BaseModel):
    success: int
    parent: Optional[Parent]

class DeleteParentOutput(BaseModel):
    success: int

class CreatePBConnectOutput(BaseModel):
    success: int

class GetFriendsByEmailOuput(BaseModel):
    parents: Dict[str, Optional[Parent]]
