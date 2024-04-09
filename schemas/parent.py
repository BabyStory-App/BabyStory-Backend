from pydantic import BaseModel
from typing import List, Optional,Dict
from model.parent import Parent

class CreateParentInput(BaseModel):
    parent_id: str
    password: str
    email: str
    name: str
    nickname: str
    signInMethod: str
    emailVerified: str
    photoId: str
    description: str

class CreateParentOutput(BaseModel):
    parent : Parent


class GetParentByEmailOutput(BaseModel):
    parent : Optional[Parent]


class UpdateParentInput(BaseModel):
    password: str
    email: str
    name: str
    nickname: str
    signInMethod: str
    emailVerified: str
    photoId: str
    description: str
    
class DeleteParentInput(BaseModel):
    id:int

class GetFriendsByEmailOuput(BaseModel):
    parents: Dict[str, Optional[Parent]]