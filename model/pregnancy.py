from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
import uuid

from model.parent import Parent
from model.baby import Baby

# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | pregn_id  | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | baby_id   | varchar(255) | NO   | MUL | NULL    |                |
# | dname     | varchar(50)  | YES  |     | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+
# CREATE TABLE pregnancy (
#     pregn_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     baby_id VARCHAR(255) NOT NULL,
#     dname VARCHAR(50),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id),
#     FOREIGN KEY (baby_id) REFERENCES baby(baby_id)
# );

class Pregnancy(BaseModel):
    pregn_id: int
    parent_id: str
    baby_id: str
    dname: str

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class PregnancyTable(DB_Base):
    __tablename__ = 'pregnancy'

    pregn_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'))
    baby_id = Column(String(255), ForeignKey('baby.baby_id'))
    dname = Column(String(50))

    parent = relationship(Parent, back_populates='pregnancy', passive_deletes=True)
    baby = relationship(Baby, back_populates='pregnancy', passive_deletes=True)