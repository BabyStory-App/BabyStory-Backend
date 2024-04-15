from sqlalchemy import Column,String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base

from model.parent import ParentTable
from model.baby import BabyTable

# 유저와 아이를 연결하는 테이블
# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | pbc_id    | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | baby_id   | varchar(255) | NO   | MUL | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+
# CREATE TABLE pbconnect(
#     pbc_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     baby_id VARCHAR(255) NOT NULL,
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id),
#     FOREIGN KEY (baby_id) REFERENCES baby(baby_id)
# );


class PBConnect(BaseModel):
    pbc_id: int
    parent_id: str
    baby_id: str

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class PBConnectTable(DB_Base):
    __tablename__ = 'pbconnect'

    pbc_id = Column(Integer, primary_key=True, nullable=False,autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'))
    baby_id = Column(String(255), ForeignKey('baby.baby_id'))

    
    parent = relationship(ParentTable, backref='pbconnect', passive_deletes=True)
    baby = relationship(BabyTable, backref='pbconnect', passive_deletes=True)