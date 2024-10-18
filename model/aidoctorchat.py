from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from model.parent import ParentTable


# AI 의사 채팅 테이블
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | id         | int          | NO   | PRI | NULL    | auto_increment |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |                |
# | room_id    | int          | NO   | MUL | NULL    |                |
# | createTime | datetime     | NO   |     | NULL    |                |
# | ask        | text         | NO   |     | NULL    |                |
# | res        | text         | NO   |     | NULL    |                |
# | hospital   | json         | YES  |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+


class AIDoctorChat(BaseModel):
    id: int
    parent_id: str
    room_id: int
    createTime: datetime
    ask: str
    res: str
    hospital: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class AIDoctorChatTable(DB_Base):
    __tablename__ = 'aidoctorchat'

    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    room_id = Column(Integer, ForeignKey(
        'aidoctorroom.id'), nullable=False)
    createTime = Column(DateTime, nullable=False)
    ask = Column(Text, nullable=False)
    res = Column(Text, nullable=False)
    hospital = Column(JSON, nullable=True)
