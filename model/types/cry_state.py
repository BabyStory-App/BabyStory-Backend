from pydantic import BaseModel, constr
from typing import Optional
from uuid import uuid4
from datetime import datetime
from pydantic.types import Json
from enum import Enum

from model.types.common import OptionalBaseUUID, OptionalBaseId


class CryIntensity(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'


class CryType(str, Enum):
    sad = 'sad'
    hug = 'hug'
    diaper = 'diaper'
    hungry = 'hungry'
    sleepy = 'sleepy'
    awake = 'awake'
    uncomfortable = 'uncomfortable'


class CryStateType_id(BaseModel):
    id: OptionalBaseId


class CryStateType_babyId(BaseModel):
    babyId: OptionalBaseUUID = uuid4()


class CryStateType_time(BaseModel):
    time: datetime


class CryStateType_type(BaseModel):
    type: CryType = CryType.uncomfortable


class CryStateType_audioId(BaseModel):
    audioId: str


class CryStateType_predictMap(BaseModel):
    predictMap: Json


class CryStateType_intensity(BaseModel):
    intensity: Optional[CryIntensity] = CryIntensity.medium


class CryStateType_duration(BaseModel):
    duration: Optional[float] = 2.0


class CryStateModel(CryStateType_id,
                    CryStateType_babyId,
                    CryStateType_time,
                    CryStateType_type,
                    CryStateType_audioId,
                    CryStateType_predictMap,
                    CryStateType_intensity,
                    CryStateType_duration):

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
