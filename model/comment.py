# 게시물 댓글 테이블

from sqlalchemy import Column, Integer, String, DateTime, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional

from model.post import PostTable
from model.parent import ParentTable
from model.comment import CommentTable

# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | comment_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |                |
# | post_id    | int(11)      | NO   | MUL | NULL    |                |
# | reply_id   | int(11)      | YES  | MUL | NULL    |                |
# | comment    | text         | NO   |     | NULL    |                |
# | time       | datetime     | NO   |     | NULL    |                |
# | cheart     | int(11)      | YES  |     | 0       |                |
# +------------+--------------+------+-----+---------+----------------+
# CREATE TABLE comment(
#     comment_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     post_id INT NOT NULL,
#     reply_id INT DEFAULT NULL,
#     comment TEXT NOT NULL,
#     time DATETIME NOT NULL,
#     cheart INT DEFAULT 0,
#     FOREIGN KEY (post_id) REFERENCES post(post_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id),
#     FOREIGN KEY (reply_id) REFERENCES comment(comment_id)
# );

class Comment(BaseModel):
    comment_id: int
    parent_id: str
    post_id: int
    reply_id: int
    comment: TEXT
    time: datetime
    cheart: Optional[int]

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
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.post_id'), nullable=False)
    reply_id = Column(Integer, ForeignKey('comment.comment_id'), nullable=True)
    comment = Column(TEXT, nullable=False)
    time = Column(DateTime, nullable=False)
    cheart = Column(Integer)

    post = relationship(PostTable, backref='comment', passive_deletes=True)
    parent = relationship(ParentTable, backref='comment', passive_deletes=True)
    comment = relationship(CommentTable, backref='comment', passive_deletes=True)