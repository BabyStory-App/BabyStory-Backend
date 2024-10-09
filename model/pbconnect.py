from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from model.parent import ParentTable
from model.baby import BabyTable


# 유저와 아이를 연결하는 테이블
# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | pbc_id    | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | baby_id   | varchar(255) | NO   | MUL | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+


class PBConnect(BaseModel):
    pbc_id: int
    parent_id: str
    baby_id: str

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class PBConnectTable(DB_Base):
    __tablename__ = 'pbconnect'

    pbc_id = Column(Integer, primary_key=True,
                    nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    baby_id = Column(String(255), ForeignKey('baby.baby_id'), nullable=False)

    parent = relationship(
        ParentTable, backref='pbconnect', passive_deletes=True)
    baby = relationship(BabyTable, backref='pbconnect', passive_deletes=True)
