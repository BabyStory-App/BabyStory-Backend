from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from model.pcomment import PCommentTable, PComment
from schemas.pcomment import *

from db import get_db_session

class CommentService:
    def __init__(self):
        # 댓글 리스트
        self.comment_list = []

    # 댓글 생성
    def createPComment(self, createPCommentInput: CreatePCommentInput,parent_id: str) -> Optional[PComment]:
        """
        댓글 생성
        --input
            - createPCommentInput.comment_id: 댓글 아이디
            - createPCommentInput.post_id: 게시물 아이디
            - createPCommentInput.reply_id: 상위 댓글 아이디
            - createPCommentInput.comment: 댓글 내용
            - createPCommentInput.time: 댓글 생성 시간
            - createPCommentInput.cheart: 댓글 하트 수
            - parent_id: 부모 댓글 아이디
        --output
            - Comment: 댓글
        """
        db = get_db_session()
        try:
            comment = PCommentTable(
                comment_id=createPCommentInput.comment_id,
                parent_id=parent_id,
                post_id=createPCommentInput.post_id,
                reply_id=createPCommentInput.reply_id,
                comment=createPCommentInput.comment,
                time=createPCommentInput.time,
                cheart=createPCommentInput.cheart,
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
    def updatePComment(self, parent_id: str, 
                      updatePCommentInput: UpdatePCommentInput) -> Optional[PComment]:
        """
        댓글 수정
        --input
            - parent_id: 부모 아이디
            - updatePCommentInput.comment_id: 댓글 아이디
            - updatePCommentInput.comment: 댓글 내용
        --output
            - Comment: 댓글
        """
        db = get_db_session()
        try:
            comment = db.query(PCommentTable).filter(
                PCommentTable.comment_id == updatePCommentInput.comment_id,
                PCommentTable.parent_id==parent_id).first()
            
            if comment is None:
                return None

            # comment를 수정
            setattr(comment, 'comment', updatePCommentInput.comment)
            # time을 현재 시간으로 수정
            setattr(comment, 'time', updatePCommentInput.time)

            db.add(comment)
            db.commit()
            db.refresh(comment)

            return comment
        
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(status_code=400, detail="updateComment error")
        
    # 댓글 삭제
    def deletePComment(self, parent_id: str, 
                      deletePCommentInput: DeletePCommentInput) -> Optional[PComment]:
        """
        댓글 삭제
        --input
            - parent_id: 부모 아이디
            - deletePCommentInput.comment_id: 댓글 아이디
            - deletePCommentInput.time: 댓글 삭제 시간 datetime.now()
        --output
            - Comment: 댓글
        """
        db = get_db_session()
        try:
            comment = db.query(PCommentTable).filter(
                PCommentTable.comment_id == deletePCommentInput.comment_id,
                PCommentTable.parent_id==parent_id).first()
            
            if comment is None:
                return None
            
            # time을 현재 시간으로 수정
            setattr(comment, 'time', deletePCommentInput.time)

            db.add(comment)
            db.commit()
            db.refresh(comment)

            return comment
        
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(status_code=400, detail="deleteComment error")
    
    # 재귀적으로 댓글을 가져오는 함수
    def getPCommentRecursive(self, comment: PCommentTable) -> PComment:
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