from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.post import *

# 게시물 생성
class CreatePostInput(BaseModel):
    post_id: str
    post: str
    photos: Optional[str]
    post_time: datetime
    modify_time: Optional[datetime]
    delete_time: Optional[datetime]
    heart: Optional[int]
    share: Optional[int]
    script: Optional[int]
    comment: Optional[int]
    hash: Optional[str]

class CreatePostOutput(BaseModel):
    post: Optional[Post]

# 게시물 수정
class UpdatePostInput(BaseModel):
    post_id: str
    post: str
    photos: Optional[str]
    post_time: datetime
    modify_time: datetime = datetime.now()
    delete_time: Optional[datetime]
    hash: Optional[str]

class UpdatePostOutput(BaseModel):
    success: int
    post: Optional[Post]
    
# 게시물 삭제
class DeletePostInput(BaseModel):
    post_id: str
    post: str
    photos: Optional[str]
    post_time: datetime
    modify_time: Optional[datetime]
    delete_time: datetime = datetime.now()
    hash: Optional[str]

class DeletePostOutput(BaseModel):
    success: int
    post: Optional[Post]
