# 실시간 채팅 말풍선 테이블

from sqlalchemy import Column, Integer, String, DateTime, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base

from model.chat import ChatTable
from model.parent import ParentTable

# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | chat_id   | int(11)      | NO   | PRI | NULL    | auto_increment |
# | room_id   | int(11)      | NO   | MUL | NULL    |                |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | time      | datetime     | YES  |     | NULL    |                |
# | chat_type | varchar(255) | YES  |     | NULL    |                |
# | content   | text         | YES  |     | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+
# CREATE TABLE chatbubble (
#     chat_id INT PRIMARY KEY auto_increment NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     room_id INT NOT NULL,
#     time DATETIME NOT NULL,
#     chat_type VARCHAR(255) NOT NULL,
#     content TEXT NOT NULL,
#     FOREIGN KEY (room_id) REFERENCES chat(room_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );

class Chatbubble(BaseModel):
    chat_id: int
    parent_id: str
    room_id: int
    time: DateTime
    chat_type: str
    content: TEXT

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class ChatbubbleTable(DB_Base):
    __tablename__ = 'chatbubble'

    chat_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    room_id = Column(Integer, ForeignKey('chat.room_id'), nullable=False)
    time = Column(DateTime, nullable=False)
    chat_type = Column(String(255), nullable=False)
    content = Column(TEXT, nullable=False)

    chat = relationship(ChatTable, back_populates='chatbubble', passive_deletes=True)
    parent = relationship(ParentTable, back_populates='chatbubble', passive_deletes=True)