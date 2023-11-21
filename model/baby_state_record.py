from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from db import DB_Base
import uuid


class BabyStateRecord(DB_Base):
    __tablename__ = 'baby_state_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    babyId = Column(String(36), ForeignKey(
        'baby.id', ondelete='SET NULL'))
    recordDate = Column(DateTime, nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    weight = Column(Float)
    height = Column(Float)
    headCircumference = Column(Float)
    photoId = Column(Text)

# parent -> baby -> baby_state_record -> cry_state


# CREATE TABLE baby_state_record (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     babyId VARCHAR(36),
#     recordDate DATETIME NOT NULL,
#     title VARCHAR(255) NOT NULL,
#     description TEXT,
#     weight FLOAT,
#     height FLOAT,
#     headCircumference FLOAT,
#     photoId TEXT,
#     INDEX (recordDate),
#     INDEX (title),
#     FULLTEXT INDEX (description),
#     FOREIGN KEY (babyId) REFERENCES baby(id) ON DELETE SET NULL
# );
