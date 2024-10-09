from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from model.purchase import PurchaseTable
from model.parent import ParentTable


# 공동구매 조회 테이블
# +-------------+--------------+------+-----+---------+----------------+
# | Field       | Type         | Null | Key | Default | Extra          |
# +-------------+--------------+------+-----+---------+----------------+
# | jview_id    | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id   | varchar(255) | NO   | MUL | NULL    |                |
# | purchase_id | int(11)      | NO   | MUL | NULL    |                |
# | createTime  | datetime     | YES  |     | NULL    |                |
# +-------------+--------------+------+-----+---------+----------------+


class Jview(BaseModel):
    jview_id: int
    parent_id: str
    purchase_id: int
    createTime: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class JviewTable(DB_Base):
    __tablename__ = 'jview'

    jview_id = Column(Integer, primary_key=True,
                      nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    purchase_id = Column(Integer, ForeignKey(
        'purchase.purchase_id'), nullable=False)
    createTime = Column(datetime, nullable=False)

    parent = relationship(
        ParentTable, back_populates='jview', passive_deletes=True)
    view = relationship(
        PurchaseTable, back_populates='jview', passive_deletes=True)
