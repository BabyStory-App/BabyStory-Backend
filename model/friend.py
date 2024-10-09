from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from model.parent import ParentTable


# 유저간의 친구 테이블
# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | friend_id | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | friend    | varchar(255) | NO   | MUL | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+


class Friend(BaseModel):
    friend_id: int
    parent_id: str
    friend: str

    class Config:
        from_attributes = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class FriendTable(DB_Base):
    __tablename__ = 'friend'

    friend_id = Column(Integer, primary_key=True,
                       nullable=False, autoincrement=True)
    parent_id = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)
    friend = Column(String(255), ForeignKey(
        'parent.parent_id'), nullable=False)

    # parent = relationship(ParentTable, back_populates='friend', passive_deletes=True)
    # friend = relationship(ParentTable, back_populates='friend', passive_deletes=True)
    parent = relationship("ParentTable", foreign_keys=[
                          parent_id], back_populates='friends')
    friend_parent = relationship("ParentTable", foreign_keys=[
                                 friend], back_populates='friend_of', uselist=False)


ParentTable.friends = relationship("FriendTable", foreign_keys=[
                                   FriendTable.parent_id], back_populates="parent", passive_deletes=True)
ParentTable.friend_of = relationship("FriendTable", foreign_keys=[
                                     FriendTable.friend], back_populates="friend_parent", passive_deletes=True)
