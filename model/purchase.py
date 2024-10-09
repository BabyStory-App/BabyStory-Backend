from sqlalchemy import Column, String, ForeignKey, Integer, TEXT, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional
from model.parent import ParentTable


# 공동구매 게시물 테이블
# +-------------+--------------+------+-----+---------+----------------+
# | Field       | Type         | Null | Key | Default | Extra          |
# +-------------+--------------+------+-----+---------+----------------+
# | purchase_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id   | varchar(255) | NO   | MUL | NULL    |                |
# | title       | varchar(100) | NO   |     | NULL    |                |
# | content     | text         | NO   |     | NULL    |                |
# | photoId     | varchar(255) | NO   |     | NULL    |                |
# | createTime  | datetime     | NO   |     | NULL    |                |
# | link        | varchar(255) | NO   |     | NULL    |                |
# | jheart      | int(11)      | YES  |     | 0       |                |
# | jview       | int(11)      | YES  |     | 0       |                |
# | joint       | int(11)      | YES  |     | 0       |                |
# +-------------+--------------+------+-----+---------+----------------+


class Purchase(BaseModel):
    purchase_id: int
    parent_id: str
    title: str
    content: Optional[str]
    photoId: str
    createTime: datetime
    link: str
    jheart: int
    jview: int
    joint: int

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class PurchaseTable(DB_Base):
    __tablename__ = 'purchase'

    purchase_id = Column(Integer, primary_key=True,
                         nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    title = Column(String(20), nullable=False)
    content = Column(TEXT, nullable=True)
    photoId = Column(String(255), nullable=False)
    createTime = Column(DateTime, nullable=False)
    link = Column(String(255), nullable=False)
    jheart = Column(Integer, nullable=True, default=0)
    jview = Column(Integer, nullable=True, default=0)
    joint = Column(Integer, nullable=True, default=0)

    parent = relationship(
        ParentTable, back_populates='purchase', passive_deletes=True)
