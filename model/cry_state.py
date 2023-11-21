from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from db import DB_Base
import uuid


class CryState(DB_Base):
    __tablename__ = 'cry_state'
    id = Column(Integer, primary_key=True, autoincrement=True)
    babyId = Column(String(36), ForeignKey(
        'baby.id', ondelete='SET NULL'))
    time = Column(DateTime, nullable=False)
    type = Column(String(50), nullable=False)
    audioId = Column(Text, nullable=False)
    predictMap = Column(JSON, nullable=False)
    intensity = Column(String(50), default='medium')
    duration = Column(Float, default=2.0)


# CREATE TABLE cry_state (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     babyId VARCHAR(36),
#     time DATETIME NOT NULL,
#     type VARCHAR(50) NOT NULL,
#     audioId TEXT NOT NULL,
#     predictMap JSON NOT NULL,
#     intensity VARCHAR(50) DEFAULT 'medium',
#     duration FLOAT DEFAULT 2.0,
#     FOREIGN KEY (babyId) REFERENCES baby(id) ON DELETE SET NULL
# );
