from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional
from model.parent import ParentTable
from model.baby import BabyTable


# 수첩 테이블
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | diary_id   | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |                |
# | baby_id    | varchar(255) | NO   | MUL | NULL    |                |
# | born       | int(11)      | NO   |     | NULL    |                |
# | title      | varchar(50)  | NO   |     | NULL    |                |
# | img        | varchar(255) | NO   |     | NULL    |                |
# | createTime | datetime     | NO   |     | NULL    |                |
# | modifyTime | datetime     | YES  |     | NULL    |                |
# | deleteTime | datetime     | YES  |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+

class Diary(BaseModel):
    diary_id: int
    parent_id: str
    baby_id: str
    born: int
    title: str
    img: str
    createTime: datetime
    modifyTime: Optional[datetime]
    deleteTime: Optional[datetime]

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class DiaryTable(DB_Base):
    __tablename__ = 'diary'

    diary_id = Column(Integer, primary_key=True,
                      nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    baby_id = Column(String(255), ForeignKey('baby.baby_id'), nullable=False)
    born = Column(Integer, nullable=False)
    title = Column(String(50), nullable=False)
    img = Column(String(255), nullable=False)
    createTime = Column(DateTime, nullable=False)
    modifyTime = Column(DateTime, nullable=True)
    deleteTime = Column(DateTime, nullable=True)

    parent = relationship(ParentTable, backref='diary', passive_deletes=True)
    baby = relationship(BabyTable, backref='diary', passive_deletes=True)
