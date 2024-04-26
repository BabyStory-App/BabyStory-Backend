# 게시물 댓글 하트

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
import uuid

from model.comment import CommentTable
from model.parent import ParentTable

# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | cheart_id  | int(11)      | NO   | PRI | NULL    | auto_increment |
# | comment_id | int(11)      | NO   | MUL | NULL    |                |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+
# CREATE TABLE cheart (
#     cheart_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     comment_id INT NOT NULL,
#     FOREIGN KEY (comment_id) REFERENCES comment(comment_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );

class Cheart(BaseModel):
    cheart_id: int
    parent_id: str
    comment_id: int

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))
    
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