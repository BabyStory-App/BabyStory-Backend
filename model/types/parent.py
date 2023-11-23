from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from uuid import uuid4

from model.types.common import OptionalBaseUUID


class ParentType_uid(BaseModel):
    uid: constr(min_length=1)


class ParentType_email(BaseModel):
    email: EmailStr


class ParentType_nickname(BaseModel):
    nickname: constr(min_length=1)


class ParentType_signInMethod(BaseModel):
    signInMethod: Optional[str] = 'email'


class ParentType_emailVerified(BaseModel):
    emailVerified: Optional[bool] = False


class ParentType_photoId(BaseModel):
    photoId: Optional[str]


class ParentType_description(BaseModel):
    description: Optional[str]


# Parent 모델 정의
class ParentType(ParentType_uid,
                 ParentType_email,
                 ParentType_nickname,
                 ParentType_signInMethod,
                 ParentType_emailVerified,
                 ParentType_photoId,
                 ParentType_description):

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)
