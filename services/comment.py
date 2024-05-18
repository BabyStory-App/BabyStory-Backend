from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from model.comment import CommentTable
from schemas.comment import *

from db import get_db_session

class CommentService:
    def __init__(self):
        self.comment_list = []

    def createComment(self, createCommentInput: CreateCommentInput) -> Optional[Comment]:
        """
        댓글 생성
        --input
            - createCommentInput.comment_id: 댓글 아이디
            - createCommentInput.parent_id: 부모 댓글 아이디
            - createCommentInput.post_id: 게시물 아이디
            - createCommentInput.reply_id: 상위 댓글 아이디
            - createCommentInput.comment: 댓글 내용
            - createCommentInput.time: 댓글 생성 시간
            - createCommentInput.cheart: 댓글 하트 수
        --output
            - Comment: 댓글
        """
        db = get_db_session()
        try:
            comment = CommentTable(
                comment_id=createCommentInput.comment_id,
                parent_id=createCommentInput.parent_id,
                post_id=createCommentInput.post_id,
                reply_id=createCommentInput.reply_id,
                comment=createCommentInput.comment,
                time=createCommentInput.time,
                cheart=createCommentInput.cheart
            )

            db.add(comment)
            db.commit()
            db.refresh(comment)

            return comment
        
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(status_code=400, detail="createComment error")
        

    def updateComment(self, parent_id: str, 
                      updateCommentInput: UpdateCommentInput) -> Optional[Comment]:
        """
        댓글 수정
        --input
            - parent_id: 부모 아이디
            - updateCommentInput.comment_id: 댓글 아이디
            - updateCommentInput.comment: 댓글 내용
        --output
            - Comment: 댓글
        """
        db = get_db_session()
        try:
            comment = db.query(CommentTable).filter(
                CommentTable.comment_id == updateCommentInput.comment_id,
                CommentTable.parent_id==parent_id).first()
            
            if comment is None:
                return None

            setattr(comment, 'comment', updateCommentInput.comment)
            # time을 현재 시간으로 수정
            setattr(comment, 'time', updateCommentInput.time)

            db.add(comment)
            db.commit()
            db.refresh(comment)

            return comment
        
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(status_code=400, detail="updateComment error")
        
    
    def deleteComment(self, parent_id: str, 
                      deleteCommentInput: DeleteCommentInput) -> Optional[Comment]:
        """
        댓글 삭제
        --input
            - parent_id: 부모 아이디
            - deleteCommentInput.comment_id: 댓글 아이디
            - deleteCommentInput.time: 댓글 삭제 시간 datetime.now()
        --output
            - Comment: 댓글
        """
        db = get_db_session()
        try:
            comment = db.query(CommentTable).filter(
                CommentTable.comment_id == deleteCommentInput.comment_id,
                CommentTable.parent_id==parent_id).first()
            
            if comment is None:
                return None
            
            # time을 현재 시간으로 수정
            setattr(comment, 'time', deleteCommentInput.time)

            db.add(comment)
            db.commit()
            db.refresh(comment)

            return comment
        
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(status_code=400, detail="deleteComment error")
    

    def getCommentRecursive(self, comment: CommentTable) -> Comment:
        db=get_db_session()
        comment_data = Comment.from_orm(comment)
        replies = db.query(CommentTable).filter(CommentTable.reply_id == comment.comment_id).all()

        if replies:
            for reply in replies:
                print(reply.comment_id)
                # 이미 추가한 댓글이 아니면 추가하고 재귀 호출
                comment_data.replies.append(self.getCommentRecursive(reply))
        
        return comment_data

    def getAllComment(self, post_id: str) -> List[Comment]:
        db=get_db_session()
        try:
            top_comments = db.query(CommentTable).filter(
                CommentTable.post_id == post_id,
                CommentTable.reply_id == None).all()

            self.comment_list = []
            
            for top_comment in top_comments:
                self.comment_list.append(self.getCommentRecursive(top_comment))
            
            return self.comment_list
            
        except Exception as e:
            raise (e)
            #raise HTTPException(status_code=400, detail="getAllComment error")