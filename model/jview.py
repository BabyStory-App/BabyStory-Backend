from sqlalchemy import Column,String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from model.purchase import PurchaseTable
from model.parent import ParentTable


class Jview(BaseModel):
    jview_id: int
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

class JviewTable(DB_Base):
    __tablename__ = 'jview'

    jview_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey('parent.parent_id'), nullable=False)
    purchase_id = Column(Integer, ForeignKey('purchase.purchase_id'), nullable=False)
    createTime = Column(DateTime, nullable=False)

    parent = relationship(ParentTable, back_populates='jview', passive_deletes=True)
    view = relationship(PurchaseTable, back_populates='jview', passive_deletes=True)