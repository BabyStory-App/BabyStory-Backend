from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from model.baby import BabyTable


# 아기 상태 테이블
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | state_id   | int(11)      | NO   | PRI | NULL    | auto_increment |
# | baby_id    | varchar(255) | NO   | MUL | NULL    |                |
# | createTime | datetime     | NO   |     | NULL    |                |
# | cm         | float        | YES  |     | NULL    |                |
# | kg         | float        | YES  |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+


class Babystate(BaseModel):
    state_id: int
    baby_id: str
    createTime: datetime
    cm: float
    kg: float

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class BabystateTable(DB_Base):
    __tablename__ = 'babystate'

    state_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    baby_id = Column(String(255), nullable=False)
    createTime = Column(DateTime, nullable=False)
    cm = Column(Float, nullable=True)
    kg = Column(Float, nullable=True)

    baby = relationship(BabyTable, back_populates='babystate', passive_deletes=True)