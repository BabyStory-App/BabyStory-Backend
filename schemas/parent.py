from pydantic import BaseModel
from typing import Optional, Dict

from model.parent import Parent


class XJWT(BaseModel):
    access_token: str


class CreateParentInput(BaseModel):
    parent_id: str
    password: str
    email: str
    nickname: str
    signInMethod: str
    emailVerified: bool


class CreateParentOutput(BaseModel):
    parent: Optional[Parent]
    x_jwt: XJWT


class GetParentByEmailOutput(BaseModel):
    parent: Optional[Parent]
    x_jwt: XJWT


class UpdateParentInput(BaseModel):
    password: str
    email: str
    name: str
    nickname: str
    gender: Optional[int]
    signInMethod: str
    emailVerified: bool
    photoId: Optional[str]
    description: Optional[str]
    mainAddr: Optional[str]
    subAddr: Optional[str]
    hashList: Optional[str]


class UpdateParentOutput(BaseModel):
    success: int
    parent: Optional[Parent]


class DeleteParentOutput(BaseModel):
    success: int


class CreatePBConnectOutput(BaseModel):
    success: int


class GetFriendsByEmailOutput(BaseModel):
    parents: Dict[str, Optional[Parent]]


class CreateLoginInput(BaseModel):
    email: str
    password: str


class CreateLoginOutput(BaseModel):
    parent: Optional[Parent]
    x_jwt: XJWT
