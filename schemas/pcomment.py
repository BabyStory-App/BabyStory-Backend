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


class CommentParent(BaseModel):
    parent_id: str
    nickname: str
    photoId: str


class CommentOutput(BaseModel):
    comment_id: int
    content: str
    createTime: datetime
    modifyTime: Optional[datetime]
    cheart: Optional[int] = 0
    replies: Optional[List["CommentOutput"]] = None
    parent: CommentParent


# 모든 댓글 가져오기
class GetAllPCommentOutput(BaseModel):
    success: int
    message: str
    post_id: int
    comments: List[CommentOutput]


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
