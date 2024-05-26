from sqlalchemy import Column, String, DateTime, Float, Integer
from sqlalchemy.orm import relationship
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from db import DB_Base
import uuid
#from model.baby_state_record import BabyStateRecord
#from model.cry_state import CryState


# 아기 테이블
# 아기 테이블
# +-----------+--------------+------+-----+---------+-------+
# | Field     | Type         | Null | Key | Default | Extra |
# +-----------+--------------+------+-----+---------+-------+
# | baby_id   | varchar(255) | NO   | PRI | NULL    |       |
# | obn       | varchar(255) | NO   |     | NULL    |       |
# | name      | varchar(255) | YES  |     | NULL    |       |
# | gender    | tinyint(3)   | YES  |     | NULL    |       |
# | gender    | tinyint(3)   | YES  |     | NULL    |       |
# | birthDate | datetime     | YES  |     | NULL    |       |
# | bloodType | char(3)      | YES  |     | NULL    |       |
# | cm        | float        | YES  |     | NULL    |       |
# | kg        | float        | YES  |     | NULL    |       |
# | cm        | float        | YES  |     | NULL    |       |
# | kg        | float        | YES  |     | NULL    |       |
# | photoId   | varchar(255) | YES  |     | NULL    |       |
# +-----------+--------------+------+-----+---------+-------+



class Baby(BaseModel):
    baby_id: str
    obn: str
    name: Optional[str]
    gender: Optional[int]
    birthDate: Optional[datetime]
    bloodType: Optional[str]
    cm: Optional[float]
    kg: Optional[float]
    cm: Optional[float]
    kg: Optional[float]
    photoId: Optional[str]

    class Config:
        orm_mode = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class BabyTable(DB_Base):
    __tablename__ = 'baby'
    baby_id = Column(String(255), primary_key=True, nullable=False, default=uuid.uuid4)
    obn = Column(String(255), nullable=False)
    name = Column(String(255), index=True)
    gender = Column(Integer, nullable=True)
    birthDate = Column(DateTime, nullable=True)
    bloodType = Column(String(3), nullable=True)
    cm = Column(Float, nullable=True)
    kg = Column(Float, nullable=True)
    photoId = Column(String(255), nullable=True)


    # Relationships
    # state_records = relationship(
    #     BabyStateRecord, backref='baby', passive_deletes=True)
    # cry_states = relationship(CryState, backref='baby', passive_deletes=True)

# CREATE TABLE baby (
#     id VARCHAR(36) NOT NULL DEFAULT (UUID()),
#     parentId VARCHAR(36),
#     name VARCHAR(255) NOT NULL,
#     gender VARCHAR(50) NOT NULL,
#     birthDate DATETIME NOT NULL,
#     bloodType VARCHAR(50) NOT NULL,
#     photoId VARCHAR(255),
#     PRIMARY KEY (id),
#     INDEX (name),
#     FOREIGN KEY (parentId) REFERENCES parent(uid) ON DELETE SET NULL
# );
