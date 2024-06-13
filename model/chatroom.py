from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from typing import Optional
from model.parent import ParentTable
from model.chatbubble import ChatbubbleTable


# 채팅방 테이블
# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | room_id   | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | lastChat  | int(11)      | NO   | MUL | NULL    |                |
# | name      | varchar(100) | NO   |     | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+


class Chat(BaseModel):
    room_id: int
    parent_id: str
    end_chat: int
    name: str
    pid: Optional[str]

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class ChatTable(DB_Base):
    __tablename__ = 'chat'

    room_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    end_chat = Column(Integer, ForeignKey('chat.chat_id'), nullable=False)
    name = Column(String(100), nullable=False)
    pid = Column(String(255), nullable=True)
    
    parent = relationship(ParentTable, back_populates='chat', passive_deletes=True)
    chat = relationship(ChatbubbleTable, back_populates='chat', passive_deletes=True)