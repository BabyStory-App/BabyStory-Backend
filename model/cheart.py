from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from model.comment import CommentTable
from model.parent import ParentTable


# 게시물 댓글 하트 테이블
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | cheart_id  | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |                |
# | comment_id | int(11)      | NO   | MUL | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+


class Cheart(BaseModel):
    cheart_id: int
    parent_id: str
    comment_id: int
    
    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class CheartTable(DB_Base):
    __tablename__ = 'cheart'

    cheart_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    comment_id = Column(Integer, ForeignKey('comment.comment_id'), nullable=False)
    
    comment = relationship(CommentTable, back_populates='cheart', passive_deletes=True)
    parent = relationship(ParentTable, back_populates='cheart', passive_deletes=True)