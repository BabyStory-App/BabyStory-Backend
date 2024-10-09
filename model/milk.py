from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional
from model.diary import DiaryTable


# 수유일지 테이블
# +---------+----------+------+-----+---------+----------------+
# | Field   | Type     | Null | Key | Default | Extra          |
# +---------+----------+------+-----+---------+----------------+
# | milk_id | int(11)  | NO   | PRI | NULL    | auto_increment |
# | dday_id | int(11)  | NO   | MUL | NULL    |                |
# | milk    | int(11)  | NO   |     | NULL    |                |
# | mamount | int(11)  | NO   |     | NULL    |                |
# | mtime   | datetime | NO   |     | NULL    |                |
# +---------+----------+------+-----+---------+----------------+

class Milk(BaseModel):
    milk_id: int
    dday_id: int
    milk: int
    mamount: int
    mtime: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class MilkTable(DB_Base):
    __tablename__ = 'milk'

    milk_id = Column(Integer, primary_key=True,
                     nullable=False, autoincrement=True)
    dday_id = Column(Integer, ForeignKey('dday.dday_id'), nullable=False)
    milk = Column(Integer, nullable=False)
    mamount = Column(Integer, nullable=False)
    mtime = Column(DateTime, nullable=False)

    dday = relationship(DiaryTable, backref='milk', passive_deletes=True)
