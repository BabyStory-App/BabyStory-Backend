from sqlalchemy import Column,String, ForeignKey, Integer, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from model.baby import BabyTable


# 울음 기록 테이블
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | babycry_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | baby_id    | varchar(255) | NO   | MUL | NULL    |                |
# | createTime | datetime     | YES  |     | NULL    |                |
# | cryType    | varchar(50)  | YES  |     | NULL    |                |
# | audioId    | char(36)     | YES  |     | NULL    |                |
# | predictMap | json         | YES  |     | NULL    |                |
# | intensity  | tinyint(3)   | YES  |     | NULL    |                |
# | duration   | float        | YES  |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+


class Babycry(BaseModel):
    babycry_id: int
    baby_id: str
    createTime: datetime
    cryType: str
    audioId: str
    predictMap: dict
    intensity: int
    duration: float

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class BabycryTable(DB_Base):
    __tablename__ = 'babycry'

    babycry_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    baby_id = Column(String(255), ForeignKey('baby.baby_id'), nullable=False)
    createTime = Column(DateTime, nullable=True)
    cryType = Column(String(50), nullable=True)
    audioId = Column(String(36), nullable=True)
    predictMap = Column(JSON, nullable=True)
    intensity = Column(Integer, nullable=True)
    duration = Column(Float, nullable=True)

    baby = relationship(BabyTable, back_populates='babycry', passive_deletes=True)