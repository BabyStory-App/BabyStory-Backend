from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.hospital import *

# 산모수첩 생성
class CreateHospitalInput(BaseModel):
    diary_id: int
    baby_id: str
    parent_kg: float
    bpressure: float
    baby_kg: Optional[float] = None
    baby_cm: Optional[int] = None
    special: Optional[str] = None
    next_day: Optional[datetime] = None

class CreateHospitalOutput(BaseModel):
    success: int
    message: str
    hospital: Hospital