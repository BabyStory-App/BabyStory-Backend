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
    password: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    nickname: Optional[str] = None
    gender: Optional[int] = None
    signInMethod: Optional[str] = None
    emailVerified: Optional[bool] = None
    photoId: Optional[str] = None
    description: Optional[str] = None
    mainAddr: Optional[str] = None
    subAddr: Optional[str] = None
    hashList: Optional[str] = None


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


class UploadProfileImageOutput(BaseModel):
    success: int
    photoId: str
