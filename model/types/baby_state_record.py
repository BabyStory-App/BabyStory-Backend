from pydantic import BaseModel, constr
from typing import Optional
from uuid import uuid4
from datetime import datetime

from model.types.common import OptionalBaseId, OptionalBaseUUID


class BabyStateRecordType_id(BaseModel):
    id: OptionalBaseId


class BabyStateRecordType_babyId(BaseModel):
    babyId: OptionalBaseUUID = uuid4()


class BabyStateRecordType_recordDate(BaseModel):
    recordDate: datetime


class BabyStateRecordType_title(BaseModel):
    title: constr(min_length=1)


class BabyStateRecordType_description(BaseModel):
    description: Optional[str]


class BabyStateRecordType_weight(BaseModel):
    weight: Optional[float]


class BabyStateRecordType_height(BaseModel):
    height: Optional[float]


class BabyStateRecordType_headCircumference(BaseModel):
    headCircumference: Optional[float]


class BabyStateRecordType_photoId(BaseModel):
    photoId: Optional[str]


class BabyStateRecordType(BabyStateRecordType_id,
                          BabyStateRecordType_babyId,
                          BabyStateRecordType_recordDate,
                          BabyStateRecordType_title,
                          BabyStateRecordType_description,
                          BabyStateRecordType_weight,
                          BabyStateRecordType_height,
                          BabyStateRecordType_headCircumference,
                          BabyStateRecordType_photoId):

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)
