from sqlalchemy import Column,String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from model.deal import DealTable
from model.parent import ParentTable


# 중고거래 조회수 테이블
# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | dheart_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | deal_id   | int(11)      | NO   | MUL | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+


class Dview(BaseModel):
    view_id: int
    parent_id: str
    deal_id: int
    createTime: datetime

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class DviewTable(DB_Base):
    __tablename__ = 'dview'

    view_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    deal_id = Column(Integer, ForeignKey('deal.deal_id'), nullable=False)
    createTime = Column(DateTime, nullable=False)

    parent = relationship(ParentTable, back_populates='dview', passive_deletes=True)
    deal = relationship(DealTable, back_populates='dview', passive_deletes=True)