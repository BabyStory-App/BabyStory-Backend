# 중고거래 위시리스트 테이블

from sqlalchemy import Column,String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional

from model.deal import DealTable
from model.parent import ParentTable
# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | dheart_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | deal_id   | int(11)      | NO   | MUL | NULL    |                |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+
# CREATE TABLE dheart (
#     dheart_id INT PRIMARY KEY auto_increment NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     deal_id INT NOT NULL,
#     FOREIGN KEY (deal_id) REFERENCES deal(deal_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );

class Dheart(BaseModel):
    dheart_id: int
    parent_id: str
    deal_id: int

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class DheartTable(DB_Base):
    __tablename__ = 'dheart'

    dheart_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    deal_id = Column(Integer, ForeignKey('deal.deal_id'), nullable=False)

    parent = relationship(ParentTable, back_populates='dheart', passive_deletes=True)
    deal = relationship(DealTable, back_populates='dheart', passive_deletes=True)