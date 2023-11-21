from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from db import DB_Base
import uuid

from model.baby import Baby


class Parent(DB_Base):
    __tablename__ = 'parent'
    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    uid = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), nullable=False, index=True)
    nickname = Column(String(255), nullable=False)
    signInMethod = Column(String(50), default='email')
    emailVerified = Column(Boolean, default=False)
    photoId = Column(Text)
    description = Column(Text)

    # Relationship to Baby
    babies = relationship(Baby, backref='parent', passive_deletes=True)

# CREATE TABLE parent (
#     id VARCHAR(36) NOT NULL DEFAULT (UUID()),
#     uid VARCHAR(255) UNIQUE NOT NULL,
#     email VARCHAR(255) NOT NULL,
#     nickname VARCHAR(255) NOT NULL,
#     signInMethod VARCHAR(50) DEFAULT 'email',
#     emailVerified BOOLEAN DEFAULT FALSE,
#     photoId TEXT,
#     description TEXT,
#     PRIMARY KEY (id),
#     INDEX (email)
# );
