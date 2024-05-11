from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.post import *

# 게시물 생성
class CreatePostInput(BaseModel):
    title: str
    post: str
    photos: Optional[str]
    post_time: datetime = datetime.now()
    hash: Optional[str]

class CreatePostOutput(BaseModel):
    post: Optional[Post]

# 게시물 수정
class UpdatePostInput(BaseModel):
    post_id: int
    title: str
    post: str
    photos: Optional[str]
    modify_time: datetime = datetime.now()
    hash: Optional[str]

class UpdatePostOutput(BaseModel):
    success: int
    post: Post
    
# 게시물 삭제
class DeletePostInput(BaseModel):
    post_id: int
    delete_time: datetime = datetime.now()

class DeletePostOutput(BaseModel):
    success: int
    post: Optional[Post]