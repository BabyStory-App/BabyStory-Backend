# 게시물 테이블

from sqlalchemy import Column, Integer, String, DateTime, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
from typing import Optional

from model.parent import ParentTable

# +-------------+------------------+------+-----+---------+----------------+
# | Field       | Type             | Null | Key | Default | Extra          |
# +-------------+------------------+------+-----+---------+----------------+
# | post_id     | int(11)          | NO   | PRI | NULL    | auto_increment |
# | parent_id   | varchar(255)     | NO   | MUL | NULL    |                |
# | post        | text             | NO   |     | NULL    |                |
# | photos      | text             | YES  |     | NULL    |                |
# | post_time   | datetime         | NO   |     | NULL    |                |
# | modify_time | datetime         | YES  |     | NULL    |                |
# | delete_time | datetime         | YES  |     | NULL    |                |
# | heart       | int(10) unsigned | YES  |     | NULL    |                |
# | share       | int(10) unsigned | YES  |     | NULL    |                |
# | script      | int(10) unsigned | YES  |     | NULL    |                |
# | comment     | int(10) unsigned | YES  |     | NULL    |                |
# | hash        | varchar(100)     | YES  |     | NULL    |                |
# +-------------+------------------+------+-----+---------+----------------+
# CREATE TABLE post (
#     post_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     post TEXT NOT NULL,
#     photos TEXT,
#     post_time DATETIME NOT NULL,
#     modify_time DATETIME,
#     delete_time DATETIME,
#     heart INT UNSIGNED,
#     share INT UNSIGNED,
#     script INT UNSIGNED,
#     comment INT UNSIGNED,
#     hash VARCHAR(100),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );


class Post(BaseModel):
    post_id: int
    parent_id: str
    post: TEXT
    photos: Optional[TEXT]
    post_time: datetime
    modify_time: Optional[datetime]
    delete_time: Optional[datetime]
    heart: Optional[int]
    share: Optional[int]
    script: Optional[int]
    comment: Optional[int]
    hash: Optional[str]

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class PostTable(DB_Base):
    __tablename__ = 'post'

    post_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    post = Column(TEXT, nullable=False)
    photos = Column(TEXT)
    post_time = Column(DateTime, nullable=False)
    modify_time = Column(DateTime)
    delete_time = Column(DateTime)
    heart = Column(Integer)
    share = Column(Integer)
    script = Column(Integer)
    comment = Column(Integer)
    hash = Column(String(100))

    parent = relationship(ParentTable, backref='post', passive_deletes=True)