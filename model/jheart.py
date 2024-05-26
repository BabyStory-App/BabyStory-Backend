from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from model.purchase import PurchaseTable
from model.parent import ParentTable


class JHeart(BaseModel):
    jheart_id: int
    parent_id: str
    purchase_id: int
    createTime: datetime

    class Config:
        orm_mode = True
        use_enum_values = True
    
    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class JHeartTable(DB_Base):
    __tablename__ = 'jheart'

    pheart_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.post_id'), nullable=False)
    createTime = Column(DateTime, nullable=False)

    view = relationship(PurchaseTable, backref='jheart', passive_deletes=True)
    parent = relationship(ParentTable, backref='jheart', passive_deletes=True)