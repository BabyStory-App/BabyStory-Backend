from pydantic import BaseModel
from typing import Optional, Dict

from model.friend import Friend


class CreateFriendInput(BaseModel):
    friend: str
    
# class CreateParentOutput(BaseModel):
#     parent: Optional[Parent]
#     x_jwt: str


# class GetParentByEmailOutput(BaseModel):
#     parent: Optional[Parent]
#     x_jwt: str


# class UpdateParentInput(BaseModel):
#     password: str
#     email: str
#     name: str
#     nickname: str
#     gender: Optional[int]
#     signInMethod: str
#     emailVerified: int
#     photoId: Optional[str]
#     description: Optional[str]
#     mainAddr: Optional[str]
#     subAddr: Optional[str]
#     hashList: Optional[str]

# class UpdateParentOutput(BaseModel):
#     success: int
#     parent: Optional[Parent]

# class DeleteParentOutput(BaseModel):
#     success: int

# class CreatePBConnectOutput(BaseModel):
#     success: int

# class GetFriendsByEmailOutput(BaseModel):
#     parents: Dict[str, Optional[Parent]]
