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
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | end_chat  | int(11)      | NO   | MUL | NULL    |                |
# | name      | varchar(100) | NO   |     | NULL    |                |
# | pid       | varchar(255) | YES  |     | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+
# CREATE TABLE chat (
#     room_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     end_chat INT NOT NULL,
#     name VARCHAR(100) NOT NULL,
#     pid VARCHAR(255),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );

# 마지막 채팅 채팅말풍선이랑 연결
# ALTER TABLE chat
# ADD CONSTRAINT fk_end_chat
# FOREIGN KEY (end_chat) REFERENCES chatbubble(chat_id);

class Chat(BaseModel):
    room_id: int
    parent_id: str
    end_chat: str
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
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    end_chat = Column(Integer, ForeignKey('chat.chat_id'), nullable=False)
    name = Column(String(100), nullable=False)
    pid = Column(String(255))
    
    parent = relationship(ParentTable, back_populates='chat', passive_deletes=True)
    chat = relationship(ChatbubbleTable, back_populates='chat', passive_deletes=True)