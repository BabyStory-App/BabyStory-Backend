from pydantic import BaseModel, constr
from typing import Optional
from uuid import uuid4
from datetime import datetime
from enum import Enum

from model.types.common import OptionalBaseUUID


class Gender(str, Enum):
    male = 'male'
    female = 'female',
    unknown = 'unknown'


class BloodType(str, Enum):
    a = 'a'
    b = 'b'
    o = 'o'
    ab = 'ab'
    unknown = 'unknown'


class BabyType_id(BaseModel):
    id: OptionalBaseUUID = uuid4()


class BabyType_parentId(BaseModel):
    parentId: constr(min_length=1)


class BabyType_name(BaseModel):
    name: constr(min_length=1)


class BabyType_gender(BaseModel):
    gender: Gender = Gender.unknown


class BabyType_birthDate(BaseModel):
    birthDate: datetime


class BabyType_bloodType(BaseModel):
    bloodType: BloodType = BloodType.unknown


class BabyType(BabyType_id,
               BabyType_parentId,
               BabyType_name,
               BabyType_gender,
               BabyType_birthDate,
               BabyType_bloodType):

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
