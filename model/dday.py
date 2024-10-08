from sqlalchemy import Column, Integer, String, DateTime, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional
from model.diary import DiaryTable


# 태교 & 육아일기 테이블
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | dday_id    | int(11)      | NO   | PRI | NULL    | auto_increment |
# | diary_id   | int(11)      | NO   | MUL | NULL    |                |
# | title      | varchar(50)  | NO   |     | NULL    |                |
# | picture    | varchar(255) | YES  |     | NULL    |                |
# | post       | text         | YES  |     | NULL    |                |
# | createTime | datetime     | NO   |     | NULL    |                |
# | modifyTime | datetime     | YES  |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+

class Dday(BaseModel):
    dday_id: int
    diary_id: int
    title: str
    picture: Optional[str]
    post: Optional[str]
    createTime: datetime
    modifyTime: Optional[datetime]

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class DdayTable(DB_Base):
    __tablename__ = 'dday'

    dday_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    diary_id = Column(Integer, ForeignKey('diary.diary_id'), nullable=False)
    title = Column(String(50), nullable=False)
    picture = Column(String(255), nullable=True)
    post = Column(TEXT, nullable=True)
    createTime = Column(DateTime, nullable=False)
    modifyTime = Column(DateTime, nullable=True)

    diary = relationship(DiaryTable, backref='dday', passive_deletes=True)