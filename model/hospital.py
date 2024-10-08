from sqlalchemy import Column, Integer, String, DateTime, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional
from model.dday import DdayTable


# 산모수첩 테이블
# +-------------+--------------+------+-----+---------+----------------+
# | Field       | Type         | Null | Key | Default | Extra          |
# +-------------+--------------+------+-----+---------+----------------+
# | hospital_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | dday_id     | int(11)      | NO   | MUL | NULL    |                |
# | createTime  | datetime     | NO   |     | NULL    |                |
# | modifyTime  | datetime     | YES  |     | NULL    |                |
# | parent_kg   | float        | NO   |     | NULL    |                |
# | bpressure   | float        | NO   |     | NULL    |                |
# | baby_kg     | float        | YES  |     | NULL    |                |
# | baby_cm     | int(11)      | YES  |     | NULL    |                |
# | special     | text         | YES  |     | NULL    |                |
# | next_day    | datetime     | YES  |     | NULL    |                |
# | ultrasound  | varchar(255) | YES  |     | NULL    |                |
# | uvideo      | varchar(255) | YES  |     | NULL    |                |
# +-------------+--------------+------+-----+---------+----------------+

class Hospital(BaseModel):
    hospital_id: int
    dday_id: int
    createTime: datetime
    modifyTime: Optional[datetime]
    parent_kg: float
    bpressure: float
    baby_kg: Optional[float]
    baby_cm: Optional[int]
    special: Optional[str]
    next_day: Optional[datetime]
    ultrasound: Optional[str]
    uvideo: Optional[str]

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class HospitalTable(DB_Base):
    __tablename__ = 'hospital'

    hospital_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    dday_id = Column(Integer, ForeignKey('dday.dday_id'), nullable=False)
    createTime = Column(DateTime, nullable=False)
    modifyTime = Column(DateTime, nullable=True)
    parent_kg = Column(Integer, nullable=False)
    bpressure = Column(Integer, nullable=False)
    baby_kg = Column(Integer, nullable=True)
    baby_cm = Column(Integer, nullable=True)
    special = Column(TEXT, nullable=True)
    next_day = Column(DateTime, nullable=True)
    ultrasound = Column(String(255), nullable=True)
    uvideo = Column(String(255), nullable=True)

    dday = relationship(DdayTable, backref='hospital', passive_deletes=True)