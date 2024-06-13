from sqlalchemy import Column, Integer, String, DateTime, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from model.chat import ChatTable
from model.parent import ParentTable


# 실시간 채팅 말풍선 테이블
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | chat_id    | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id  | varchar(255) | NO   | MUL | NULL    |                |
# | room_id    | int(11)      | NO   | MUL | NULL    |                |
# | createTime | datetime     | NO   |     | NULL    |                |
# | chatType   | varchar(255) | NO   |     | NULL    |                |
# | content    | text         | NO   |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+


class Chatbubble(BaseModel):
    chat_id: int
    parent_id: str
    room_id: int
    createTime: DateTime
    chatType: str
    content: str

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
    createTime = Column(DateTime, nullable=False)
    chatType = Column(String(255), nullable=False)
    content = Column(TEXT, nullable=False)

    chat = relationship(ChatTable, back_populates='chatbubble', passive_deletes=True)
    parent = relationship(ParentTable, back_populates='chatbubble', passive_deletes=True)