# AI 의사 테이블
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base

from model.parent import ParentTable

# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | id        | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | date      | datetime     | NO   |     | NULL    |                |
# | ask       | text         | NO   |     | NULL    |                |
# | res       | text         | NO   |     | NULL    |                |
# | haddr     | text         | YES  |     | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+
# CREATE TABLE aidoctor (
# id INT PRIMARY KEY auto_increment NOT NULL,
# parent_id VARCHAR(255) NOT NULL,
# date DATETIME NOT NULL,
# ask text NOT NULL,
# res text NOT NULL,
# haddr text,
# FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );

class AIDoctor(BaseModel):
    id: int
    parent_id: str
    date: datetime
    ask_id: str
    res_id: str
    haddr: Optional[str]

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
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    date = Column(DateTime, nullable=False)
    ask_id = Column(String(100), nullable=False)
    res_id = Column(String(100), nullable=False)
    haddr = Column(String(255))

    parent = relationship(ParentTable, back_populates='aidoctor', passive_deletes=True)