from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional
from model.diary import DiaryTable


# 수유일지 테이블
# +----------+--------------+------+-----+---------+----------------+
# | Field    | Type         | Null | Key | Default | Extra          |
# +----------+--------------+------+-----+---------+----------------+
# | milk_id  | int(11)      | NO   | PRI | NULL    | auto_increment |
# | diary_id | int(11)      | NO   | MUL | NULL    |                |
# | baby_id  | varchar(255) | NO   |     | NULL    |                |
# | milk     | int(11)      | NO   |     | NULL    |                |
# | amount   | int(11)      | NO   |     | NULL    |                |
# | mtime    | datetime     | NO   |     | NULL    |                |
# +----------+--------------+------+-----+---------+----------------+

class Milk(BaseModel):
    milk_id: int
    diary_id: int
    baby_id: str
    milk: int
    amount: int
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

    milk_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    diary_id = Column(Integer, ForeignKey('diary.diary_id'), nullable=False)
    baby_id = Column(String(255), nullable=False)
    milk = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    mtime = Column(DateTime, nullable=False)

    diary = relationship(DiaryTable, backref='milk', passive_deletes=True)