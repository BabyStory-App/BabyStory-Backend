# 게시물 스트립트 테이블

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base

from model.post import PostTable
from model.parent import ParentTable

# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | script_id | int(11)      | NO   | PRI | NULL    |       |
# | post_id   | int(11)      | NO   | MUL | NULL    |       |
# | parent_id | varchar(255) | NO   | MUL | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+
# CREATE TABLE script (
#     script_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
#     parent_id VARCHAR(255) NOT NULL,
#     post_id INT NOT NULL,
#     FOREIGN KEY (post_id) REFERENCES post(post_id),
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id)
# );

class Script(BaseModel):
    script_id: int
    parent_id: str
    post_id: int

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class ScriptTable(DB_Base):
    __tablename__ = 'script'

    script_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.post_id'), nullable=False)

    post = relationship(PostTable, backref='script', passive_deletes=True)
    parent = relationship(ParentTable, backref='script', passive_deletes=True)