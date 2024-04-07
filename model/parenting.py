# 육아일기 테이블

from sqlalchemy import Column,String, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
import uuid

from model.parent import Parent
from model.baby import Baby

# +--------------+--------------+------+-----+---------+----------------+
# | Field        | Type         | Null | Key | Default | Extra          |
# +--------------+--------------+------+-----+---------+----------------+
# | parenting_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id    | varchar(255) | NO   | MUL | NULL    |                |
# | baby_id      | varchar(255) | NO   | MUL | NULL    |                |
# | ptitle       | varchar(50)  | YES  |     | NULL    |                |
# +--------------+--------------+------+-----+---------+----------------+
# CREATE TABLE parenting (
#     parenting_id INT PRIMARY KEY auto_increment NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     baby_id VARCHAR(255) NOT NULL,
#     ptitle VARCHAR(50),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id),
#     FOREIGN KEY (baby_id) REFERENCES baby(baby_id)
# );

class Parenting(BaseModel):
    parenting_id: int
    parent_id: str
    baby_id: str
    ptitle: str

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class ParentingTable(DB_Base):
    __tablename__ = 'parenting'

    parenting_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'))
    baby_id = Column(String(255), ForeignKey('baby.baby_id'))
    ptitle = Column(String(50))

    parent = relationship(Parent, back_populates='parenting', passive_deletes=True)
    baby = relationship(Baby, back_populates='parenting', passive_deletes=True)