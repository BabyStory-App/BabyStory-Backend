from sqlalchemy import Column,String, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional
from model.pregnancy import PregnancyTable


# 산모수첩 ( 병원 ) 테이블
# +-------------+--------------+------+-----+---------+----------------+
# | Field       | Type         | Null | Key | Default | Extra          |
# +-------------+--------------+------+-----+---------+----------------+
# | hospital_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | pregn_id    | int(11)      | NO   | MUL | NULL    |                |
# | hday        | datetime     | NO   |     | NULL    |                |
# | parent_kg   | float        | NO   |     | NULL    |                |
# | bpressure   | float        | NO   |     | NULL    |                |
# | special     | varchar(50)  | YES  |     | NULL    |                |
# | baby_kg     | float        | YES  |     | NULL    |                |
# | baby_heart  | int(11)      | YES  |     | NULL    |                |
# | ultrasound  | varchar(255) | YES  |     | NULL    |                |
# | uvideo      | varchar(255) | YES  |     | NULL    |                |
# +-------------+--------------+------+-----+---------+----------------+


class Phospital(BaseModel):
    hospital_id: int
    pregn_id: int
    hday: datetime
    parent_kg: float
    bpressure: float
    special: Optional[str]
    baby_kg: Optional[float]
    baby_heart: Optional[int]
    ultrasound: Optional[str]
    uvideo: Optional[str]

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class PhospitalTable(DB_Base):
    __tablename__ = 'phospital'

    hospital_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    pregn_id = Column(Integer, ForeignKey('pregnancy.pregn_id'), nullable=False)
    hday = Column(DateTime, nullable=False)
    parent_kg = Column(Float, nullable=False)
    bpressure = Column(Float, nullable=False)
    special = Column(String(50), nullable=True)
    baby_kg = Column(Float, nullable=True)
    baby_heart = Column(Integer, nullable=True)
    ultrasound = Column(String(255), nullable=True)
    uvideo = Column(String(255), nullable=True)

    pregnancy = relationship(PregnancyTable, backref='phospital', passive_deletes=True)