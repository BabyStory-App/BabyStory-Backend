from sqlalchemy import Column, String, Integer, TEXT, ForeignKey, DateTime, Boolean
from typing import Optional
from pydantic import BaseModel
from db import DB_Base
from datetime import datetime


# 구독자 알림 테이블
# +---------------+--------------+------+-----+---------+----------------+
# | Field         | Type         | Null | Key | Default | Extra          |
# +---------------+--------------+------+-----+---------+----------------+
# | id            | int          | NO   | PRI | NULL    | auto_increment |
# | creater_id    | varchar(255) | NO   | MUL | NULL    |                |
# | subscriber_id | varchar(255) | NO   | MUL | NULL    |                |
# | createTime    | datetime     | NO   |     | NULL    |                |
# +---------------+--------------+------+-----+---------+----------------+


class AlertSubscribe(BaseModel):
    id: int
    creater_id: str
    subscriber_id: str
    createTime: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class AlertSubscribeTable(DB_Base):
    __tablename__ = 'alertsub'

    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement=True)
    creater_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    subscriber_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    createTime = Column(DateTime, nullable=False)

    # parent = relationship(
    #     ParentTable, back_populates='alert', passive_deletes=True)
