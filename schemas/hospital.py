from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.hospital import *

class Hospitals(BaseModel):
    hospital_id: int
    diary_id: int
    baby_id: str
    createTime: datetime
    modifyTime: Optional[datetime]  = None
    parent_kg: float
    bpressure: float
    baby_kg: Optional[float]
    baby_cm: Optional[int]
    special: Optional[dict]
    next_day: Optional[datetime]


# 산모수첩 생성
class CreateHospitalInput(BaseModel):
    diary_id: int
    createTime: str
    parent_kg: float
    bpressure: float
    baby_kg: Optional[float] = None 
    baby_cm: Optional[int] = None
    special: Optional[str] = None
    next_day: Optional[str] = None

class CreateHospitalOutput(BaseModel):
    success: int
    message: str
    hospital: Hospital


# 범위에 대한 전체 산모수첩 조회
class GetHospitalRangeOutput(BaseModel):
    success: int
    message: str
    hospitals: List[Hospitals]


# 모든 산모수첩 조회
class GetAllHospitalOutput(BaseModel):
    success: int
    message: str
    hospitals: List[Hospitals]
    

# 하나의 산모수첩 조회
class GetHospitalOutput(BaseModel):
    success: int
    message: str
    hospital: Hospitals


# 산모수첩 수정
class UpdateHospitalInput(BaseModel):
    hospital_id: int
    parent_kg: float
    bpressure: float
    baby_kg: Optional[float] = None
    baby_cm: Optional[int] = None
    special: Optional[str] = None
    next_day: Optional[datetime] = None

class UpdateHospitalOutput(BaseModel):
    success: int
    message: str
    hospital: Hospital


# 산모수첩 삭제
class DeleteHospitalOutput(BaseModel):
    success: int
    message: str