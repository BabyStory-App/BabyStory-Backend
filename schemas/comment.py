from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.pcomment import *

class CreateCommentInput(BaseModel):
    comment_id: int
    post_id: int
    reply_id: Optional[int]
    comment: str
    time: datetime = datetime.now()
    cheart: int

class UpdateCommentInput(BaseModel):
    comment_id: int
    comment: str
    time: datetime = datetime.now()

class UpdateCommentOutput(BaseModel):
    success: int
    comment: Optional[PComment]

class DeleteCommentInput(BaseModel):
    comment_id: int
    time: datetime = datetime.now()

class DeleteCommentOutput(BaseModel):
    success: int
    comment: Optional[PComment]
