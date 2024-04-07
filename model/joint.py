# 공동거래 테이블

from sqlalchemy import Column,String, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
import uuid

from model.purchase import Purchase
from model.parent import Parent

# +-------------+--------------+------+-----+---------+----------------+
# | Field       | Type         | Null | Key | Default | Extra          |
# +-------------+--------------+------+-----+---------+----------------+
# | joint_id    | int(11)      | NO   | PRI | NULL    | auto_increment |
# | purchase_id | int(11)      | NO   | MUL | NULL    |                |
# | parent_id   | varchar(255) | NO   | MUL | NULL    |                |
# +-------------+--------------+------+-----+---------+----------------+
# CREATE TABLE joint (
#     joint_id INT PRIMARY KEY auto_increment NOT NULL,
#     purchase_id INT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     FOREIGN KEY (purchase_id) REFERENCES purchase(purchase_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );

class Joint(BaseModel):
    joint_id: int
    purchase_id: int
    parent_id: str

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class JointTable(DB_Base):
    __tablename__ = 'joint'

    joint_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    purchase_id = Column(Integer, ForeignKey('purchase.purchase_id'))
    parent_id = Column(String(255), ForeignKey('parent.parent_id'))

    purchase = relationship(Purchase, back_populates='joint', passive_deletes=True)
    parent = relationship(Parent, back_populates='joint', passive_deletes=True)