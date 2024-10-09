from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from model.post import PostTable
from model.parent import ParentTable


# 게시물 하트 테이블
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | pheart_id  | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |                |
# | post_id    | int(11)      | NO   | MUL | NULL    |                |
# | createTime | datetime     | YES  |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+


class PHeart(BaseModel):
    pheart_id: int
    parent_id: str
    post_id: int
    createTime: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class PHeartTable(DB_Base):
    __tablename__ = 'pheart'

    pheart_id = Column(Integer, primary_key=True,
                       nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.post_id'), nullable=False)
    createTime = Column(DateTime, nullable=True)

    post = relationship(PostTable, backref='pheart', passive_deletes=True)
    parent = relationship(ParentTable, backref='pheart', passive_deletes=True)
