from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from model.alertsub import *
from model.alert import *


# 알림
class GetCheckAlertOutput(BaseModel):
    status: int
    message: str


class Creater(BaseModel):
    parent_id: str
    nickname: str
    photo_id: str


class GetAlertListOutput(BaseModel):
    alert_id: int
    alert_type: Optional[str]
    message: str
    creater: Creater
    action: Optional[Dict[str, Any]] = None


class GetAlertOutput(BaseModel):
    status: int
    message: str
    createTime: datetime
    alerts: List[GetAlertListOutput]


class GetToggleSubscribeOutput(BaseModel):
    hasSubscribe: bool
    message: str
