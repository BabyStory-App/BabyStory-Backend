from sqlalchemy import Column, Integer, String, DateTime, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional
from model.parent import ParentTable


# 게시물 테이블
# +-------------+------------------+------+-----+---------+----------------+
# | Field       | Type             | Null | Key | Default | Extra          |
# +-------------+------------------+------+-----+---------+----------------+
# | post_id     | int(11)          | NO   | PRI | NULL    | auto_increment |
# | parent_id   | varchar(255)     | NO   | MUL | NULL    |                |
# | title       | varchar(144)     | NO   |     | NULL    |                |
# | photo       | text             | YES  |     | NULL    |                |
# | post_time   | datetime         | NO   |     | NULL    |                |
# | modify_time | datetime         | YES  |     | NULL    |                |
# | delete_time | datetime         | YES  |     | NULL    |                |
# | heart       | int(10) unsigned | YES  |     | NULL    |                |
# | share       | int(10) unsigned | YES  |     | NULL    |                |
# | script      | int(10) unsigned | YES  |     | NULL    |                |
# | comment     | int(10) unsigned | YES  |     | NULL    |                |
# | hash        | varchar(100)     | YES  |     | NULL    |                |
# +-------------+------------------+------+-----+---------+----------------+


class Post(BaseModel):
    post_id: int
    parent_id: str
    title: str
    photo: Optional[str]
    post_time: datetime
    modify_time: Optional[datetime]
    delete_time: Optional[datetime]
    heart: Optional[int]
    share: Optional[int]
    script: Optional[int]
    comment: Optional[int]
    hash: Optional[str]

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class PostTable(DB_Base):
    __tablename__ = 'post'

    post_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    title = Column(String(144), nullable=False)
    photo = Column(TEXT, nullable=True)
    post_time = Column(DateTime, nullable=False)
    modify_time = Column(DateTime, nullable=True)
    delete_time = Column(DateTime, nullable=True)
    heart = Column(Integer, nullable=True)
    share = Column(Integer, nullable=True)
    script = Column(Integer, nullable=True)
    comment = Column(Integer, nullable=True)
    hash = Column(String(100), nullable=True)

    parent = relationship(ParentTable, backref='post', passive_deletes=True)