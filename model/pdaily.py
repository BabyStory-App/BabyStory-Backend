# 육아일기 테이블

from sqlalchemy import Column,String, ForeignKey, Integer, TEXT, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional

from model.parenting import ParentingTable
# +--------------+--------------+------+-----+---------+----------------+
# | Field        | Type         | Null | Key | Default | Extra          |
# +--------------+--------------+------+-----+---------+----------------+
# | daily_id     | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parenting_id | int(11)      | NO   | MUL | NULL    |                |
# | daily        | datetime     | NO   |     | NULL    |                |
# | title        | varchar(50)  | YES  |     | NULL    |                |
# | picture      | varchar(255) | YES  |     | NULL    |                |
# | post         | text         | YES  |     | NULL    |                |
# +--------------+--------------+------+-----+---------+----------------+
# CREATE TABLE pdaily (
#     daily_id INT PRIMARY KEY auto_increment NOT NULL,
#     parenting_id INT NOT NULL,
#     daily DATETIME NOT NULL,
#     title VARCHAR(50) NOT NULL,
#     picture VARCHAR(255),
#     post TEXT,
#     FOREIGN KEY (parenting_id) REFERENCES parenting(parenting_id)
# );

class Pdaily(BaseModel):
    daily_id: int
    parenting_id: int
    daily: datetime
    title: str
    picture: Optional[str]
    post: Optional[TEXT]

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class PdailyTable(DB_Base):
    __tablename__ = 'pdaily'

    daily_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parenting_id = Column(Integer, ForeignKey('parenting.parenting_id'), nullable=False)
    daily = Column(DateTime, nullable=False)
    title = Column(String(50), nullable=False)
    picture = Column(String(255))
    post = Column(TEXT)
    
    parenting = relationship(ParentingTable, back_populates='pdaily', passive_deletes=True)