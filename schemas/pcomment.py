from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.pcomment import *

# 댓글 생성
class CreatePCommentInput(BaseModel):
    comment_id: int
    post_id: int
    reply_id: Optional[int]
    content: str

class CreatePCommentOutput(BaseModel):
    pcomment: Optional[PComment]

# 댓글 수정
class UpdatePCommentInput(BaseModel):
    comment_id: int
    content: str
    modifyTime: datetime = datetime.now()

class UpdatePCommentOutput(BaseModel):
    success: int
    pcomment: PComment

# 댓글 삭제
class DeletePCommentInput(BaseModel):
    comment_id: int
    deleteTime: datetime = datetime.now()

class DeletePCommentOutput(BaseModel):
    success: int
    pcomment: Optional[PComment]
