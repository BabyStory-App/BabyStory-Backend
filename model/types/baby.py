from pydantic import BaseModel, constr
from typing import Optional
from uuid import uuid4
from datetime import datetime

from model.types.common import OptionalBaseUUID


class BabyType_id(BaseModel):
    id: OptionalBaseUUID = uuid4()


class BabyType_parentId(BaseModel):
    parentId: OptionalBaseUUID = uuid4()


class BabyType_name(BaseModel):
    name: constr(min_length=1)


class BabyType_gender(BaseModel):
    gender: constr(min_length=1)


class BabyType_birthDate(BaseModel):
    birthDate: datetime


class BabyType_bloodType(BaseModel):
    bloodType: constr(min_length=1)


class BabyType(BabyType_id,
               BabyType_parentId,
               BabyType_name,
               BabyType_gender,
               BabyType_birthDate,
               BabyType_bloodType):
    class Config:
        orm_mode = True
