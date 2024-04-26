# 공동구매 게시물 테이블

from sqlalchemy import Column,String, ForeignKey, Integer, TEXT, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional

from model.parent import ParentTable

# +-------------+--------------+------+-----+---------+----------------+
# | Field       | Type         | Null | Key | Default | Extra          |
# +-------------+--------------+------+-----+---------+----------------+
# | purchase_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id   | varchar(255) | NO   | MUL | NULL    |                |
# | title       | varchar(20)  | NO   |     | NULL    |                |
# | post        | text         | YES  |     | NULL    |                |
# | img         | varchar(255) | NO   |     | NULL    |                |
# | time        | datetime     | NO   |     | NULL    |                |
# | link        | varchar(255) | NO   |     | NULL    |                |
# +-------------+--------------+------+-----+---------+----------------+
# CREATE TABLE purchase (
#     purchase_id INT PRIMARY KEY auto_increment NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     title VARCHAR(20) NOT NULL,
#     post TEXT,
#     img VARCHAR(255) NOT NULL,
#     time DATETIME NOT NULL,
#     link VARCHAR(255) NOT NULL,
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );

class Purchase(BaseModel):
    purchase_id: int
    parent_id: str
    title: int
    post: Optional[TEXT]
    img: str
    time: datetime
    link: str

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class PurchaseTable(DB_Base):
    __tablename__ = 'purchase'

    purchase_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    title = Column(Integer, nullable=False)
    post = Column(TEXT)
    img = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)
    link = Column(String(255), nullable=False)

    parent = relationship(ParentTable, back_populates='purchase', passive_deletes=True)