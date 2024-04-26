from sqlalchemy import Column,String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
import uuid

from model.parent import ParentTable

# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | friend_id  | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id1 | varchar(255) | NO   | MUL | NULL    |                |
# | parent_id2 | varchar(255) | NO   | MUL | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+
# CREATE TABLE friend (
#     friend_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
#     parent_id1 VARCHAR(255) NOT NULL,
#     parent_id2 VARCHAR(255) NOT NULL,
#     FOREIGN KEY (parent_id1) REFERENCES parent(parent_id),
#     FOREIGN KEY (parent_id2) REFERENCES parent(parent_id)
# );

class Friend(BaseModel):
    friend_id: int
    parent_id1: str
    parent_id2: str

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class FriendTable(DB_Base):
    __tablename__ = 'friend'

    friend_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id1 = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    parent_id2 = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)

    parent1 = relationship(ParentTable, back_populates='friend', passive_deletes=True)
    parent2 = relationship(ParentTable, back_populates='friend', passive_deletes=True)