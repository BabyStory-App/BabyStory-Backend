# 유저와 채팅방을 연결하는 테이블

from sqlalchemy import Column,String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
import uuid

from model.ppconnect import PPConnect
from model.parent import Parent

# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | pcc_id    | int(11)      | NO   | PRI | NULL    |       |
# | ppc_id    | int(11)      | NO   | MUL | NULL    |       |
# | parent_id | varchar(255) | NO   | MUL | NULL    |       |
# | room_id   | int(11)      | NO   | MUL | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+
# CREATE TABLE pcconnect (
#     pcc_id INT PRIMARY KEY NOT NULL,
#     ppc_id INT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     room_id INT NOT NULL,
#     FOREIGN KEY (ppc_id) REFERENCES ppconnect(ppc_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id),
#     FOREIGN KEY (room_id) REFERENCES chat(room_id)
# );

class PCConnect(BaseModel):
    pcc_id: int
    ppc_id: int
    parent_id: str
    room_id: int

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class PCConnectTable(DB_Base):
    __tablename__ = 'pcconnect'

    pcc_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ppc_id = Column(Integer, ForeignKey('ppconnect.ppc_id'))
    parent_id = Column(String(255), ForeignKey('parent.parent_id'))
    room_id = Column(Integer, ForeignKey('chat.room_id'))

    ppc = relationship(PPConnect, backref='pcconnect', passive_deletes=True)
    parent = relationship(Parent, backref='pcconnect', passive_deletes=True)
    # 채팅방 정보 추가