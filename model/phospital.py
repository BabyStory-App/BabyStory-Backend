# 산모수첩 ( 병원 ) 테이블

from sqlalchemy import Column,String, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional

from model.pregnancy import PregnancyTable

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
# CREATE TABLE phospital (
#     hospital_id INT PRIMARY KEY auto_increment NOT NULL,
#     pregn_id INT NOT NULL,
#     hday DATETIME NOT NULL,
#     parent_kg FLOAT NOT NULL,
#     bpressure FLOAT NOT NULL,
#     special VARCHAR(50),
#     baby_kg FLOAT,
#     baby_heart INT,
#     ultrasound VARCHAR(255),
#     uvideo VARCHAR(255),
#     FOREIGN KEY (pregn_id) REFERENCES pregnancy(pregn_id)
# );

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

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

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
    special = Column(String(50))
    baby_kg = Column(Float)
    baby_heart = Column(Integer)
    ultrasound = Column(String(255))
    uvideo = Column(String(255))

    pregnancy = relationship(PregnancyTable, backref='phospital', passive_deletes=True)