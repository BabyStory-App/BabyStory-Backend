from fastapi import HTTPException
from typing import Optional, List
from sqlalchemy.orm import joinedload

from model.comment import Comment

from schemas.comment import *

from db import get_db_session

class CommentService:
    def createComment(self, createCommentInput: CreateCommentInput) -> Comment:
        db = get_db_session()
        try:
            comment = CommentTable(
                comment_id=createCommentInput.comment_id,
                post_id=createCommentInput.post_id,
                parent_id=createCommentInput.parent_id,
                comment=createCommentInput.comment,
                comment_time=createCommentInput.comment_time,
                modify_time=None,
                delete_time=None
            )

            db.add(comment)
            db.commit()
            db.refresh(comment)

            return comment
        
        except Exception as e:
            db.rollback()
            print(e)
            raise Exception("Failed to create comment")