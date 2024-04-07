# 산모수첩 ( 일기 ) 테이블

from sqlalchemy import Column,String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime
import uuid

from model.pregnancy import Pregnancy


# +----------+--------------+------+-----+---------+----------------+
# | Field    | Type         | Null | Key | Default | Extra          |
# +----------+--------------+------+-----+---------+----------------+
# | daily_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | pregn_id | int(11)      | NO   | MUL | NULL    |                |
# | daily    | datetime     | NO   |     | NULL    |                |
# | title    | varchar(50)  | YES  |     | NULL    |                |
# | picture  | varchar(255) | YES  |     | NULL    |                |
# | post     | text         | YES  |     | NULL    |                |
# +----------+--------------+------+-----+---------+----------------+
# CREATE TABLE pregndaily (
#     daily_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
#     pregn_id INT NOT NULL,
#     daily DATETIME NOT NULL,
#     title VARCHAR(50),
#     picture VARCHAR(255),
#     post TEXT,
#     FOREIGN KEY (pregn_id) REFERENCES pregnancy(pregn_id)
# );

class Pregndaily(BaseModel):
    daily_id: int
    pregn_id: int
    daily: datetime
    title: str
    picture: str
    post: str

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class PregndailyTable(DB_Base):
    __tablename__ = 'pregndaily'

    daily_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    pregn_id = Column(Integer, ForeignKey('pregnancy.pregn_id'))
    daily = Column(DateTime, nullable=False)
    title = Column(String(50))
    picture = Column(String(255))
    post = Column(String(255))

    pregnancy = relationship(Pregnancy, back_populates='pregndaily', passive_deletes=True)