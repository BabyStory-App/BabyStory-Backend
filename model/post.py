from sqlalchemy import Column, Integer, String, DateTime, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional
from model.parent import ParentTable


# 게시물 테이블
# +------------+------------------+------+-----+---------+----------------+
# | Field      | Type             | Null | Key | Default | Extra          |
# +------------+------------------+------+-----+---------+----------------+
# | post_id    | int(11)          | NO   | PRI | NULL    | auto_increment |
# | parent_id  | varchar(255)     | NO   | MUL | NULL    |                |
# | reveal     | tinyint(4)       | NO   |     | NULL    |                |
# | title      | varchar(144)     | NO   |     | NULL    |                |
# | content    | text             | NO   |     | NULL    |                |
# | photoId    | text             | YES  |     | NULL    |                |
# | createTime | datetime         | NO   |     | NULL    |                |
# | modifyTime | datetime         | YES  |     | NULL    |                |
# | deleteTime | datetime         | YES  |     | NULL    |                |
# | pHeart     | int(10) unsigned | YES  |     | 0       |                |
# | pScript    | int(10) unsigned | YES  |     | 0       |                |
# | pView      | int(10) unsigned | YES  |     | 0       |                |
# | pComment   | int(10) unsigned | YES  |     | 0       |                |
# | hashList   | varchar(100)     | YES  |     | NULL    |                |
# +------------+------------------+------+-----+---------+----------------+


class Post(BaseModel):
    post_id: int
    parent_id: str
    reveal: int
    title: str
    content: str
    photoId: Optional[str]
    createTime: datetime
    modifyTime: Optional[datetime]
    deleteTime: Optional[datetime]
    pHeart: Optional[int]
    pScript: Optional[int]
    pView: Optional[int]
    pComment: Optional[int]
    hashList: Optional[str]

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
    reveal = Column(Integer, nullable=False)
    title = Column(String(144), nullable=False)
    content = Column(TEXT, nullable=False)
    photoId = Column(TEXT, nullable=True)
    createTime = Column(DateTime, nullable=False)
    modifyTime = Column(DateTime, nullable=True)
    deleteTime = Column(DateTime, nullable=True)
    pHeart = Column(Integer, nullable=True)
    pScript = Column(Integer, nullable=True)
    pView = Column(Integer, nullable=True)
    pComment = Column(Integer, nullable=True)
    hashList = Column(String(100), nullable=True)

    parent = relationship(ParentTable, backref='post', passive_deletes=True)