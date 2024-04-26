# 육아일기 테이블

from sqlalchemy import Column,String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from typing import Optional

from model.parent import ParentTable
from model.baby import BabyTable

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
#     ptitle VARCHAR(50) NOT NULL,
#     img VARCHAR(255),
#     time DATETIME NOT NULL,
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id),
#     FOREIGN KEY (baby_id) REFERENCES baby(baby_id)
# );

class Parenting(BaseModel):
    parenting_id: int
    parent_id: str
    baby_id: str
    ptitle: str
    img: Optional[str]
    time: DateTime

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
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    baby_id = Column(String(255), ForeignKey('baby.baby_id'), nullable=False)
    ptitle = Column(String(50), nullable=False)
    img = Column(String(255))
    time = Column(DateTime, nullable=False)

    parent = relationship(ParentTable, back_populates='parenting', passive_deletes=True)
    baby = relationship(BabyTable, back_populates='parenting', passive_deletes=True)