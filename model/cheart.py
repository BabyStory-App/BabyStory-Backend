from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from model.pcomment import PCommentTable
from model.parent import ParentTable


# 게시물 댓글 하트 테이블
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | cheart_id  | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |                |
# | comment_id | int(11)      | NO   | MUL | NULL    |                |
# | createTime | datetime     | NO   |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+


class CHeart(BaseModel):
    cheart_id: int
    parent_id: str
    comment_id: int
    createTime: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class CHeartTable(DB_Base):
    __tablename__ = 'cheart'

    cheart_id = Column(Integer, primary_key=True,
                       nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    comment_id = Column(Integer, ForeignKey(
        'pcomment.comment_id'), nullable=True)
    createTime = Column(DateTime, nullable=True)

    pcomment = relationship(
        PCommentTable, backref='pcheart', passive_deletes=True)
    parent = relationship(ParentTable, backref='pcheart', passive_deletes=True)
