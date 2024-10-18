from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from model.parent import ParentTable

# AI 의사 채팅방 테이블
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | id         | int          | NO   | PRI | NULL    | auto_increment |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |                |
# | createTime | datetime     | NO   |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+


class AIDoctorRoom(BaseModel):
    id: int
    parent_id: str
    createTime: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class AIDoctorRoomTable(DB_Base):
    __tablename__ = 'aidoctorroom'

    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    createTime = Column(DateTime, nullable=False)
