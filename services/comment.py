from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from model.pcomment import PCommentTable, PComment
from schemas.comment import *

from db import get_db_session

class CommentService:
    def __init__(self):
        # 댓글 리스트
        self.comment_list = []

    # 댓글 생성
    def createComment(self, createCommentInput: CreateCommentInput,parent_id: str) -> Optional[PComment]:
        """
        댓글 생성
        --input
            - createCommentInput.comment_id: 댓글 아이디
            - createCommentInput.post_id: 게시물 아이디
            - createCommentInput.reply_id: 상위 댓글 아이디
            - createCommentInput.comment: 댓글 내용
            - createCommentInput.time: 댓글 생성 시간
            - createCommentInput.cheart: 댓글 하트 수
            - parent_id: 부모 댓글 아이디
        --output
            - Comment: 댓글
        """
        db = get_db_session()
        try:
            comment = PCommentTable(
                comment_id=createCommentInput.comment_id,
                parent_id=parent_id,
                post_id=createCommentInput.post_id,
                reply_id=createCommentInput.reply_id,
                comment=createCommentInput.comment,
                time=createCommentInput.time,
                cheart=createCommentInput.cheart,
                replies=[]
            )

            db.add(comment)
            db.commit()
            db.refresh(comment)

            return comment
        
        except Exception as e:
            db.rollback()
            raise (e)
            #raise HTTPException(status_code=400, detail="createComment error")
        
    # 댓글 수정
    def updateComment(self, parent_id: str, 
                      updateCommentInput: UpdateCommentInput) -> Optional[PComment]:
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
            comment = db.query(PCommentTable).filter(
                PCommentTable.comment_id == updateCommentInput.comment_id,
                PCommentTable.parent_id==parent_id).first()
            
            if comment is None:
                return None

            # comment를 수정
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
        
    # 댓글 삭제
    def deleteComment(self, parent_id: str, 
                      deleteCommentInput: DeleteCommentInput) -> Optional[PComment]:
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
            comment = db.query(PCommentTable).filter(
                PCommentTable.comment_id == deleteCommentInput.comment_id,
                PCommentTable.parent_id==parent_id).first()
            
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
    
    # 재귀적으로 댓글을 가져오는 함수
    def getCommentRecursive(self, comment: PCommentTable) -> PComment:
        '''
        재귀적으로 댓글을 가져오는 함수
        --input
            - comment: 댓글
        --output
            - Comment: 댓글
        '''
        try:
            # 댓글의 대댓글을 가져옴
            comment_data = PComment.from_orm(comment)
            
            return comment_data
        
        except Exception as e:
            raise (e)
            #raise HTTPException(status_code=400, detail="getCommentRecursive error")

    # 해당 게시물의 모든 댓글 가져오기
    def getAllComment(self, post_id: str) -> List[PComment]:
        '''
        해당 게시물의 모든 댓글 가져오기
        --input
            - post_id: 게시물 아이디
        --output
            - List<Comment>: 댓글 리스트
        '''
        db=get_db_session()
        try:
            # 해당 게시물의 최상위 댓글을 가져옴
            top_comments = db.query(PCommentTable).filter(
                PCommentTable.post_id == post_id,
                PCommentTable.reply_id == None).all()

            # 댓글 리스트 초기화
            self.comment_list = []
            
            # 최상위 댓글부터 재귀적으로 댓글을 가져옴
            for top_comment in top_comments:
                self.comment_list.append(self.getCommentRecursive(top_comment))
            
            return self.comment_list
            
        except Exception as e:
            raise (e)
            #raise HTTPException(status_code=400, detail="getAllComment error")