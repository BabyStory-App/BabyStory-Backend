from pydantic import BaseModel
from typing import Optional

from model.pcomment import *


# 댓글 생성
class CreatePCommentInput(BaseModel):
    post_id: int
    reply_id: Optional[int] = None
    content: str

class CreatePCommentOutput(BaseModel):
    pcomment: Optional[PComment] = None


# 댓글 수정
class UpdatePCommentInput(BaseModel):
    comment_id: int
    content: str

class UpdatePCommentOutput(BaseModel):
    success: int
    pcomment: PComment


# 댓글 삭제
class DeletePCommentInput(BaseModel):
    comment_id: int

class DeletePCommentOutput(BaseModel):
    success: int
    pcomment: Optional[PComment] = None
