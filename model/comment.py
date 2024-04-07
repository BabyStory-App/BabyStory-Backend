# 게시물 댓글 테이블

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
import uuid

from model.post import Post
from model.parent import Parent

# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | comment_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | post_id    | int(11)      | NO   | MUL | NULL    |                |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |                |
# | type       | tinyint(1)   | NO   |     | NULL    |                |
# | comment    | text         | NO   |     | NULL    |                |
# | cphoto     | varchar(255) | YES  |     | NULL    |                |
# | time       | datetime     | NO   |     | NULL    |                |
# | cheart     | int(11)      | YES  |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+
# CREATE TABLE comment (
#     comment_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
#     post_id INT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     type BOOL NOT NULL,
#     comment TEXT NOT NULL,
#     cphoto VARCHAR(255),
#     time DATETIME NOT NULL,
#     cheart INT,
#     FOREIGN KEY (post_id) REFERENCES post(post_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );

class Comment(BaseModel):
    comment_id: int
    post_id: int
    parent_id: str
    type: bool
    comment: str
    cphoto: str
    time: datetime
    cheart: int

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))
    
    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class CommentTable(DB_Base):
    __tablename__ = 'comment'

    comment_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    post_id = Column(Integer, ForeignKey('post.post_id'))
    parent_id = Column(String(255), ForeignKey('parent.parent_id'))
    type = Column(Integer, nullable=False)
    comment = Column(String(255), nullable=False)
    cphoto = Column(String(255))
    time = Column(DateTime, nullable=False)
    cheart = Column(Integer)

    post = relationship(Post, backref='comment', passive_deletes=True)
    parent = relationship(Parent, backref='comment', passive_deletes=True)