# 울음 기록 테이블

from sqlalchemy import Column,String, ForeignKey, Integer, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
import uuid

from model.baby import BabyTable

# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | babycry_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | baby_id    | varchar(255) | NO   | MUL | NULL    |                |
# | time       | datetime     | YES  |     | NULL    |                |
# | type       | varchar(50)  | YES  |     | NULL    |                |
# | audioid    | char(1)      | YES  |     | NULL    |                |
# | predictMap | json         | YES  |     | NULL    |                |
# | intensity  | varchar(50)  | YES  |     | NULL    |                |
# | duration   | float        | YES  |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+
# CREATE TABLE babycry (
#     babycry_id INT PRIMARY KEY auto_increment NOT NULL,
#     baby_id VARCHAR(255) NOT NULL,
#     time DATETIME,
#     type VARCHAR(50),
#     audioid CHAR,
#     predictMap JSON,
#     intensity VARCHAR(50),
#     duration FLOAT,
#     FOREIGN KEY (baby_id) REFERENCES baby(baby_id)
# );

class Babycry(BaseModel):
    babycry_id: int
    baby_id: str
    time: datetime
    type: str
    audioid: str
    predictMap: dict
    intensity: str
    duration: float

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

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
    baby_id = Column(String(255), ForeignKey('baby.baby_id'))
    time = Column(DateTime)
    type = Column(String(50))
    audioid = Column(String(1))
    predictMap = Column(JSON)
    intensity = Column(String(50))
    duration = Column(Float)

    baby = relationship(BabyTable, back_populates='babycry', passive_deletes=True)