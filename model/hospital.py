from sqlalchemy import Column, Integer, String, DateTime, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional
from model.diary import DiaryTable


# 산모수첩 테이블
# +-------------+--------------+------+-----+---------+----------------+
# | Field       | Type         | Null | Key | Default | Extra          |
# +-------------+--------------+------+-----+---------+----------------+
# | hospital_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | diary_id    | int(11)      | NO   | MUL | NULL    |                |
# | baby_id     | varchar(255) | NO   |     | NULL    |                |
# | createTime  | datetime     | NO   |     | NULL    |                |
# | modifyTime  | datetime     | YES  |     | NULL    |                |
# | parent_kg   | float        | NO   |     | NULL    |                |
# | bpressure   | float        | NO   |     | NULL    |                |
# | baby_kg     | float        | YES  |     | NULL    |                |
# | baby_cm     | int(11)      | YES  |     | NULL    |                |
# | special     | text         | YES  |     | NULL    |                |
# | next_day    | datetime     | YES  |     | NULL    |                |
# +-------------+--------------+------+-----+---------+----------------+

class Hospital(BaseModel):
    hospital_id: int
    diary_id: int
    baby_id: str
    createTime: Optional[datetime]
    modifyTime: Optional[datetime]
    parent_kg: float
    bpressure: float
    baby_kg: Optional[float]
    baby_cm: Optional[int]
    special: Optional[str]
    next_day: Optional[datetime]

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class HospitalTable(DB_Base):
    __tablename__ = 'hospital'

    hospital_id = Column(Integer, primary_key=True,
                         nullable=False, autoincrement=True)
    diary_id = Column(Integer, ForeignKey('diary.diary_id'), nullable=False)
    baby_id = Column(String(255), nullable=False)
    createTime = Column(DateTime, nullable=False)
    modifyTime = Column(DateTime, nullable=True)
    parent_kg = Column(Integer, nullable=False)
    bpressure = Column(Integer, nullable=False)
    baby_kg = Column(Integer, nullable=True)
    baby_cm = Column(Integer, nullable=True)
    special = Column(TEXT, nullable=True)
    next_day = Column(DateTime, nullable=True)

    # diary = relationship(DdayTable, backref='hospital', passive_deletes=True)
    diary = relationship(DiaryTable, backref='hospital', passive_deletes=True)
