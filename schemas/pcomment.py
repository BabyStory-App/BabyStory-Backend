from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.pcomment import *

class CreatePCommentInput(BaseModel):
    comment_id: int
    post_id: int
    reply_id: Optional[int]
    comment: str
    time: datetime = datetime.now()
    cheart: int

class UpdatePCommentInput(BaseModel):
    comment_id: int
    comment: str
    time: datetime = datetime.now()

class UpdatePCommentOutput(BaseModel):
    success: int
    comment: Optional[PComment]

class DeletePCommentInput(BaseModel):
    comment_id: int
    time: datetime = datetime.now()

class DeletePCommentOutput(BaseModel):
    success: int
    comment: Optional[PComment]
