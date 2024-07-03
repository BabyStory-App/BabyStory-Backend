from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from model.pcomment import PCommentTable, PComment
from schemas.pcomment import *

from db import get_db_session

class PCommentService:
    # 댓글 생성
    def createPComment(self, parent_id: str,
                       createPCommentInput: CreatePCommentInput) -> PComment:
        
        """
        댓글 생성
        --input
            - createPCommentInput.comment_id: 댓글 아이디
            - createPCommentInput.post_id: 게시물 아이디
            - createPCommentInput.reply_id: 대댓글일 경우 대댓글 부모 아이디
            - createPCommentInput.content: 댓글 내용
            - createPCommentInput.createTime: 댓글 생성 시간
            - createPCommentInput.cheart: 댓글 하트 수
        --output
            - PComment: 댓글 딕셔너리
        """

        db = get_db_session()
        
        try:
            # print(createPCommentInput)
            pcomment = PCommentTable(
                parent_id=parent_id,
                post_id=createPCommentInput.post_id,
                reply_id=None if createPCommentInput.reply_id == 0 else createPCommentInput.reply_id,
                content=createPCommentInput.content,
                createTime=datetime.now(),
                modifyTime=None,
                deleteTime=None,
                cheart=0
            )

            db.add(pcomment)
            db.commit()
            db.refresh(pcomment)

            return pcomment
        
        except Exception as e:
            db.rollback()
            raise e



    # 모든 댓글 가져오기
    def getAllPComment(self, post_id: int) -> List[PComment]:
        
        """
        모든 댓글 가져오기
        --input
            - post_id: 게시물 아이디
        --output
            - List[PComment]: 댓글 리스트
        """

        db = get_db_session()
        
        try:
            # 대댓글인 경우 제외
            pcomment = db.query(PCommentTable).filter(
                PCommentTable.post_id == post_id,
                PCommentTable.deleteTime == None,
                PCommentTable.reply_id == None).all()
            
            return pcomment
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to get all comment")
        


    # 댓글에 대댓글이 있는 경우 대댓글 가져오기
    def getReplyPComment(self, comment_id: int) -> List[PComment]:
        
        """
        댓글에 대댓글이 있는 경우 대댓글 가져오기
        --input
            - comment_id: 댓글 아이디
        --output
            - List[PComment]: 대댓글 리스트
        """

        db = get_db_session()
        
        try:
            pcomment = db.query(PCommentTable).filter(
                PCommentTable.reply_id == comment_id,
                PCommentTable.deleteTime == None).all()

            return pcomment
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to get reply comment")
        

    # 댓글 수정
    async def updatePComment(self,
                    updatePCommentInput: UpdatePCommentInput,
                    parent_id: str) -> Optional[PComment]:
        
        """
        댓글 수정
        --input
            - updatePCommentInput.comment_id: 댓글 아이디
            - updatePCommentInput.content: 댓글 내용
            - updatePCommentInput.modifyTime: 댓글 수정 시간
        --output
            - PComment: 댓글 딕셔너리
        """

        db = get_db_session()
        
        try:
            pcomment = db.query(PCommentTable).filter(
                PCommentTable.parent_id == parent_id,
                PCommentTable.comment_id == updatePCommentInput.comment_id,
                PCommentTable.deleteTime == None).first()
            
            if pcomment is None:
                return None

            pcomment.content = updatePCommentInput.content
            pcomment.modifyTime = datetime.now()

            db.add(pcomment)
            db.commit()
            db.refresh(pcomment)

            return pcomment
        
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to update comment")
        


    # 댓글 삭제
    async def deletePComment(self, 
                             deletePCommentInput: DeletePCommentInput,
                             parent_id: str) -> PComment:
        
        """
        댓글 삭제
        --input
            - deletePCommentInput.comment_id: 댓글 아이디
            - deletePCommentInput.deleteTime: 댓글 삭제 시간
        --output
            - PComment: 댓글 딕셔너리
        """

        db = get_db_session()
        
        try:
            pcomment = db.query(PCommentTable).filter(
                PCommentTable.parent_id == parent_id,
                PCommentTable.comment_id == deletePCommentInput.comment_id,
                PCommentTable.deleteTime == None).first()
            
            if pcomment is None:
                return None

            setattr(pcomment, 'deleteTime', datetime.now())

            db.add(pcomment)
            db.commit()
            db.refresh(pcomment)

            return pcomment
        
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to delete comment")