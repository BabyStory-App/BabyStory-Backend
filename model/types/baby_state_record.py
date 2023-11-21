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
    class Config:
        orm_mode = True
