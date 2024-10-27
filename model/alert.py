from sqlalchemy import Column, String, Integer, TEXT, DateTime, Boolean, JSON, ForeignKey
from typing import Optional, Dict, Any
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime

# 알림 테이블
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | alert_id   | int          | NO   | PRI | NULL    | auto_increment |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |                |
# | createTime | datetime     | NO   |     | NULL    |                |
# | hasChecked | tinyint      | NO   |     | NULL    |                |
# | createrId  | varchar(255) | YES  | MUL | NULL    |                |
# | alert_type | varchar(255) | YES  |     | NULL    |                |
# | message    | varchar(255) | NO   |     | NULL    |                |
# | action     | json         | YES  |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+


class Alert(BaseModel):
    alert_id: int
    parent_id: str
    createTime: datetime
    hasChecked: bool
    createrId: Optional[str]
    alert_type: Optional[str]
    message: str
    action: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class AlertTable(DB_Base):
    __tablename__ = 'alert'

    alert_id = Column(Integer, primary_key=True,
                      nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    createTime = Column(DateTime, nullable=False)
    hasChecked = Column(Boolean, nullable=False)
    createrId = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=True)
    alert_type = Column(String(255), nullable=True)
    message = Column(String(255), nullable=False)
    action = Column(JSON, nullable=True)
