from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.comment import *

class CreateCommentInput(BaseModel):
    comment_id: str
    parent_id: str
    post_id: str
    reply_id: str
    comment: str
    time: datetime
    cheart: int

class UpdateCommentInput(BaseModel):
    comment_id: str
    comment: str
    time: datetime = datetime.now()

class DeleteCommentInput(BaseModel):
    comment_id: str
    time: datetime = datetime.now()
