from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from db import DB_Base
import uuid

from model.baby_state_record import BabyStateRecord
from model.cry_state import CryState


class Baby(DB_Base):
    __tablename__ = 'baby'
    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    parentId = Column(String(36), ForeignKey(
        'parent.uid', ondelete='SET NULL'))
    name = Column(String(255), nullable=False, index=True)
    gender = Column(String(50), nullable=False)
    birthDate = Column(DateTime, nullable=False)
    bloodType = Column(String(50), nullable=False)

    # Relationships
    state_records = relationship(
        BabyStateRecord, backref='baby', passive_deletes=True)
    cry_states = relationship(CryState, backref='baby', passive_deletes=True)

# CREATE TABLE baby (
#     id VARCHAR(36) NOT NULL DEFAULT (UUID()),
#     parentId VARCHAR(36),
#     name VARCHAR(255) NOT NULL,
#     gender VARCHAR(50) NOT NULL,
#     birthDate DATETIME NOT NULL,
#     bloodType VARCHAR(50) NOT NULL,
#     PRIMARY KEY (id),
#     INDEX (name),
#     FOREIGN KEY (parentId) REFERENCES parent(uid) ON DELETE SET NULL
# );
