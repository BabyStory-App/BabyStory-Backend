from sqlalchemy import Column, String, Integer, TEXT, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from typing import Optional
from pydantic import BaseModel
from db import DB_Base
from model.parent import ParentTable


# 알람 테이블
# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | alert_id  | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | target    | varchar(255) | YES  | MUL | NULL    |                |
# | message   | text         | NO   |     | NULL    |                |
# | click     | tinyint(1)   | YES  |     | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+


class Alert(BaseModel):
    alert_id: int
    parent_id: str
    target: Optional[str]
    message: str
    click: bool

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class AlertTable(DB_Base):
    __tablename__ = 'alert'

    alert_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    target = Column(String(255), nullable=True)
    message = Column(TEXT, nullable=False)
    click = Column(Boolean, nullable=False, default=False)

    parent = relationship(ParentTable, back_populates='alert', passive_deletes=True)