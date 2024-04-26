# 채팅방 테이블

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from typing import Optional

from model.parent import ParentTable
from model.chatbubble import ChatbubbleTable

# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | room_id   | int(11)      | NO   | PRI | NULL    | auto_increment |
# | name      | varchar(100) | YES  |     | NULL    |                |
# | pid       | varchar(255) | YES  |     | NULL    |                |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | end_chat  | varchar(255) | YES  |     | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+
# CREATE TABLE chat (
#     room_id INT PRIMARY KEY auto_increment NOT NULL,
#     parent_id VARCHAR(255) NOT NULL FOREIGN KEY REFERENCES parent(parent_id),
#     end_chat INT FOREIGN KEY REFERENCES chatbubble(chat_id),
#     name VARCHAR(100) NOT NULL,
#     pid VARCHAR(255)
# );

class Chat(BaseModel):
    room_id: int
    parent_id: str
    end_chat: Optional[str]
    name: str
    pid: Optional[str]

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

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
    parent_id = Column(String(255), ForeignKey('parent.parent_id'))
    end_chat = Column(Integer, ForeignKey('chat.chat_id'))
    name = Column(String(100))
    pid = Column(String(255))
    
    parent = relationship(ParentTable, back_populates='chat', passive_deletes=True)
    chat = relationship(ChatbubbleTable, back_populates='chat', passive_deletes=True)