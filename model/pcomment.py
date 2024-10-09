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


class PComment(BaseModel):
    comment_id: int
    parent_id: str
    post_id: int
    reply_id: Optional[int]
    content: str
    createTime: datetime
    modifyTime: Optional[datetime]
    deleteTime: Optional[datetime]
    cheart: Optional[int]

    class Config:
        from_attributes = True
        use_enum_values = True
        from_attributes = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class PCommentTable(DB_Base):
    __tablename__ = 'pcomment'

    comment_id = Column(Integer, primary_key=True,
                        nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.post_id'), nullable=False)
    reply_id = Column(Integer, ForeignKey(
        'pcomment.comment_id'), nullable=True)
    content = Column(TEXT, nullable=False)
    createTime = Column(DateTime, nullable=False)
    modifyTime = Column(DateTime, nullable=True)
    deleteTime = Column(DateTime, nullable=True)
    cheart = Column(Integer, nullable=True)

    parent = relationship(
        "ParentTable", backref='pcomment', passive_deletes=True)
    post = relationship("PostTable", backref='pcomment', passive_deletes=True)
    replies = relationship("PCommentTable", backref=backref(
        'parent_comment', remote_side=[comment_id]))
    # post = relationship("PostTable", backref='comment', passive_deletes=True)
    # parent = relationship("ParentTable", backref='comment', passive_deletes=True)
    # comment = relationship("CommentTable", backref='comment', passive_deletes=True)
