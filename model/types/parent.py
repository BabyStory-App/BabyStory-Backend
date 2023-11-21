from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from uuid import uuid4

from model.types.common import OptionalBaseUUID


class ParentType_id(BaseModel):
    id: OptionalBaseUUID = uuid4()


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
class ParentType(ParentType_id,
                 ParentType_uid,
                 ParentType_email,
                 ParentType_nickname,
                 ParentType_signInMethod,
                 ParentType_emailVerified,
                 ParentType_photoId,
                 ParentType_description):
    class Config:
        orm_mode = True
