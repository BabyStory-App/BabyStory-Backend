from sqlalchemy import Column,String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from model.parent import ParentTable
from model.chatroom import ChatRoomTable


# 유저와 채팅방을 연결하는 테이블
# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | pcc_id    | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | room_id   | int(11)      | NO   | MUL | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+


class PCConnect(BaseModel):
    pcc_id: int
    parent_id: str
    room_id: int

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
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    room_id = Column(Integer, ForeignKey('chatroom.room_id'), nullable=False)

    parent = relationship(ParentTable, backref='pcconnect', passive_deletes=True)
    chat = relationship(ChatRoomTable, backref='pcconnect', passive_deletes=True)