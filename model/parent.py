from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from typing import Optional


# 부모 테이블
# +---------------+--------------+------+-----+---------+-------+
# | Field         | Type         | Null | Key | Default | Extra |
# +---------------+--------------+------+-----+---------+-------+
# | parent_id     | varchar(255) | NO   | PRI | NULL    |       |
# | password      | varchar(255) | NO   |     | NULL    |       |
# | email         | varchar(255) | NO   | UNI | NULL    |       |
# | name          | varchar(50)  | NO   |     | NULL    |       |
# | nickname      | varchar(255) | NO   |     | NULL    |       |
# | gender        | tinyint(3)   | YES  |     | NULL    |       |
# | signInMethod  | varchar(50)  | NO   |     | NULL    |       |
# | emailVerified | tinyint(1)   | NO   |     | NULL    |       |
# | photoId       | varchar(255) | YES  |     | NULL    |       |
# | description   | varchar(255) | YES  |     | NULL    |       |
# | mainAddr      | varchar(50)  | YES  |     | NULL    |       |
# | subAddr       | varchar(255) | YES  |     | NULL    |       |
# | hashList      | varchar(100) | YES  |     | NULL    |       |
# +---------------+--------------+------+-----+---------+-------+


class Parent(BaseModel):
    parent_id: str
    password: str
    email: str
    name: Optional[str]
    nickname: str
    gender: Optional[int]
    signInMethod: str
    emailVerified: int
    photoId: Optional[str]
    description: Optional[str]
    mainAddr: Optional[str]
    subAddr: Optional[str]
    hashList: Optional[str]

    class Config:
        orm_mode = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class ParentTable(DB_Base):
    __tablename__ = 'parent'
    parent_id = Column(String(255), primary_key=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(50), nullable=True)
    nickname = Column(String(255), nullable=False)
    gender = Column(Integer, nullable=True)
    signInMethod = Column(String(50), nullable=False)
    emailVerified = Column(Boolean, nullable=False)
    photoId = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    mainAddr = Column(String(50), nullable=True)
    subAddr = Column(String(255), nullable=True)
    hashList = Column(String(100), nullable=True)
