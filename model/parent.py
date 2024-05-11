from sqlalchemy import Column, String, Boolean
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
# | signInMethod  | varchar(50)  | NO   |     | NULL    |       |
# | emailVerified | tinyint(1)   | NO   |     | NULL    |       |
# | photoId       | varchar(255) | YES  |     | NULL    |       |
# | description   | varchar(255) | YES  |     | NULL    |       |
# +---------------+--------------+------+-----+---------+-------+
# CREATE TABLE parent(
#     parent_id VARCHAR(255) PRIMARY KEY NOT NULL,
#     password VARCHAR(255) NOT NULL,
#     email VARCHAR(255) UNIQUE NOT NULL,
#     name VARCHAR(50) NOT NULL,
#     nickname VARCHAR(255) NOT NULL,
#     signInMethod VARCHAR(50) NOT NULL,
#     emailVerified boolean NOT NULL,
#     photoId VARCHAR(255),
#     description VARCHAR(255)
# );

class Parent(BaseModel):
    parent_id: str
    password: str
    email: str
    name: str
    nickname: str
    signInMethod: str
    emailVerified: int
    photoId: Optional[str]
    description: Optional[str]
    mainaddr: Optional[str]
    subaddr: Optional[str]

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

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
    name = Column(String(50), nullable=False)
    nickname = Column(String(255), nullable=False)
    signInMethod = Column(String(50), nullable=False)
    emailVerified = Column(Boolean, nullable=False)
    photoId = Column(String(255))
    description = Column(String(255))
    mainaddr = Column(String(255))
    subaddr = Column(String(255))


# CREATE TABLE parent (
#     uid VARCHAR(255) UNIQUE NOT NULL,
#     email VARCHAR(255) NOT NULL,
#     nickname VARCHAR(255) NOT NULL,
#     signInMethod VARCHAR(50) DEFAULT 'email',
#     emailVerified BOOLEAN DEFAULT FALSE,
#     photoId TEXT,
#     description TEXT,
#     PRIMARY KEY (uid),
#     INDEX (email)
# );
