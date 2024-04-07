# 게시물 하트 테이블

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
import uuid

from model.post import Post
from model.parent import Parent

# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | pheart_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | post_id   | int(11)      | NO   | MUL | NULL    |                |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+
# CREATE TABLE pheart (
#     pheart_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
#     post_id INT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     FOREIGN KEY (post_id) REFERENCES post(post_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );

class PHeart(BaseModel):
    pheart_id: int
    post_id: int
    parent_id: str

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class PHeartTable(DB_Base):
    __tablename__ = 'pheart'

    pheart_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    post_id = Column(Integer, ForeignKey('post.post_id'))
    parent_id = Column(String(255), ForeignKey('parent.parent_id'))

    post = relationship(Post, backref='pheart', passive_deletes=True)
    parent = relationship(Parent, backref='pheart', passive_deletes=True)