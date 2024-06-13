from sqlalchemy import Column, Integer, String, DateTime, TEXT, ForeignKey
from sqlalchemy.orm import relationship, backref
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional, List


# 게시물 댓글 테이블
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | comment_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |                |
# | post_id    | int(11)      | NO   | MUL | NULL    |                |
# | reply_id   | int(11)      | YES  | MUL | NULL    |                |
# | content    | text         | NO   |     | NULL    |                |
# | createTime | datetime     | NO   |     | NULL    |                |
# | modifyTime | datetime     | YES  |     | NULL    |                |
# | deleteTime | datetime     | YES  |     | NULL    |                |
# | cheart     | int(11)      | YES  |     | 0       |                |
# +------------+--------------+------+-----+---------+----------------+



class Comment(BaseModel):
    comment_id: int
    parent_id: str
    post_id: int
    reply_id: Optional[int]
    content: str
    comment_time: datetime
    modify_time: Optional[datetime]
    delete_time: Optional[datetime]
    cheart: Optional[int]
    replies: List['Comment'] = []
    
    class Config:
        orm_mode = True
        use_enum_values = True
        from_attributes = True
    
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
    cheart = Column(Integer, nullable=True)

    replies = relationship("CommentTable", backref=backref('parent_comment', remote_side=[comment_id]))
    #post = relationship("PostTable", backref='comment', passive_deletes=True)
    #parent = relationship("ParentTable", backref='comment', passive_deletes=True)
    #comment = relationship("CommentTable", backref='comment', passive_deletes=True)