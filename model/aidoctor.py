from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from model.parent import ParentTable


# AI 의사 테이블
# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | id        | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | date      | datetime     | NO   |     | NULL    |                |
# | ask       | text         | NO   |     | NULL    |                |
# | res       | text         | NO   |     | NULL    |                |
# | haddr     | text         | YES  |     | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+


class AIDoctor(BaseModel):
    ai_id: int
    parent_id: str
    createTime: datetime
    ask: str
    res: str
    hAddr: Optional[str]

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class AIDoctorTable(DB_Base):
    __tablename__ = 'aidoctor'

    ai_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    createTime = Column(DateTime, nullable=False)
    ask_id = Column(Text, nullable=False)
    res_id = Column(Text, nullable=False)
    hAddr = Column(Text, nullable=True)

    parent = relationship(ParentTable, back_populates='aidoctor', passive_deletes=True)