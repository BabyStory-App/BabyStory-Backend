from sqlalchemy import Column,String, ForeignKey, Integer, DateTime, TEXT
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional
from model.parent import ParentTable


# 중고거래 테이블
# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | deal_id   | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | title     | varchar(20)  | NO   |     | NULL    |                |
# | post      | text         | YES  |     | NULL    |                |
# | img       | varchar(255) | NO   |     | NULL    |                |
# | price     | int(11)      | NO   |     | NULL    |                |
# | time      | datetime     | NO   |     | NULL    |                |
# | dheart    | int(11)      | YES  |     | 0       |                |
# +-----------+--------------+------+-----+---------+----------------+


class Deal(BaseModel):
    deal_id: int
    parent_id: str
    title: str
    content: Optional[str]
    photoId: str
    price: int
    createTime: datetime
    dheart: int
    dview: int

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class DealTable(DB_Base):
    __tablename__ = 'deal'

    deal_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    title = Column(String(20), nullable=False)
    content = Column(TEXT, nullable=True)
    photoId = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    createTime = Column(DateTime, nullable=False)
    dheart = Column(Integer, nullable=True)
    dview = Column(Integer, nullable=True)

    parent = relationship(ParentTable, back_populates='deal', passive_deletes=True)