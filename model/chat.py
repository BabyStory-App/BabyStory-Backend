# 채팅방 테이블

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base

from model.parent import Parent

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
#     name VARCHAR(100),
#     pid VARCHAR(255),
#     parent_id VARCHAR(255) NOT NULL,
#     end_chat VARCHAR(255)
# );
# -- 외래 키 제약 조건 삭제
# ALTER TABLE pcconnect DROP FOREIGN KEY pcconnect_ibfk_3;

# -- room_id 속성 변경
# ALTER TABLE chat MODIFY COLUMN room_id INT AUTO_INCREMENT;

class Chat(BaseModel):
    room_id: int
    name: str
    pid: str
    parent_id: str
    end_chat: str

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
    name = Column(String(100))
    pid = Column(String(255))
    parent_id = Column(String(255), ForeignKey('parent.parent_id'))
    end_chat = Column(String(255))

    parent = relationship(Parent, back_populates='chat', passive_deletes=True)