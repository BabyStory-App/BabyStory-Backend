from fastapi import HTTPException
from typing import Optional, List
from sqlalchemy.orm import joinedload

from model.comment import CommentTable
from schemas.comment import *

from db import get_db_session

class CommentService:
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
    
    def get_comments_recursive(db, post_id, comment_id, comments):
        # 대댓글 가져오기
        replies = db.query(CommentTable).filter(CommentTable.reply_id == comment_id).all()
        
        # 대댓글이 없으면 반환
        if not replies:
            return
        
        # 대댓글 리스트를 최상위 댓글 객체에 추가
        comments.extend(replies)
        
        # 각 대댓글에 대해 재귀적으로 처리
        for reply in replies:
            get_comments_recursive(db, post_id, reply.comment_id, comments)

    def getAllComment(db, post_id: str) -> Optional[List[Comment]]:
        """
        해당 게시물의 모든 댓글 가져오기
        --input
            - post_id: 게시물 아이디
        --output
            - List<Comment>: 댓글 리스트
        """
        db = get_db_session()
        try:
            # 최상위 댓글 가져오기
            top_comments = db.query(CommentTable).filter(CommentTable.post_id == post_id, CommentTable.reply_id == None).all()
            
            # 대댓글을 모두 저장할 리스트
            all_comments = []
            
            # 각 최상위 댓글에 대한 대댓글 리스트 추가
            for top_comment in top_comments:
                get_comments_recursive(db, post_id, top_comment.comment_id, all_comments)
            
            return all_comments
            
        except Exception as e:
            raise (e)
            #raise HTTPException(status_code=400, detail="getAllComment error")