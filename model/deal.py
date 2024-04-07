# 중고거래 테이블

from sqlalchemy import Column,String, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
import uuid

from model.parent import Parent

# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | deal_id   | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | title     | int(11)      | NO   |     | NULL    |                |
# | post      | text         | YES  |     | NULL    |                |
# | img       | varchar(255) | NO   |     | NULL    |                |
# | time      | datetime     | NO   |     | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+
# CREATE TABLE deal (
#     deal_id INT PRIMARY KEY auto_increment NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     title INT NOT NULL,
#     post TEXT,
#     img VARCHAR(255) NOT NULL,
#     time DATETIME NOT NULL,
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );

class Deal(BaseModel):
    deal_id: int
    parent_id: str
    title: int
    post: str
    img: str
    time: datetime

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

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
    parent_id = Column(String(255), ForeignKey('parent.parent_id'))
    title = Column(Integer, nullable=False)
    post = Column(String(255))
    img = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)

    parent = relationship(Parent, back_populates='deal', passive_deletes=True)