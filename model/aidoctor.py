# AI 의사 테이블
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base

from model.parent import Parent

# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | id        | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | ask_id    | varchar(100) | YES  |     | NULL    |                |
# | res_id    | varchar(100) | YES  |     | NULL    |                |
# | haddr     | varchar(255) | YES  |     | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+
# CREATE TABLE aidoctor (
#     id INT PRIMARY KEY auto_increment NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     ask_id VARCHAR(100),
#     res_id VARCHAR(100),
#     haddr VARCHAR(255)
# );
# ALTER TABLE aidoctor
#     ADD CONSTRAINT fk_parent_id FOREIGN KEY (parent_id) REFERENCES parent(parent_id);

class AIDoctor(BaseModel):
    id: int
    parent_id: str
    ask_id: str
    res_id: str
    haddr: str

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class AIDoctorTable(DB_Base):
    __tablename__ = 'aidoctor'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'))
    ask_id = Column(String(100))
    res_id = Column(String(100))
    haddr = Column(String(255))

    parent = relationship(Parent, back_populates='aidoctor', passive_deletes=True)