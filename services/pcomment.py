from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from db import get_db_session

from model.pcomment import PCommentTable, PComment
from schemas.pcomment import *
from error.exception.customerror import *

class PCommentService:

    # 댓글 생성
    def createPComment(self, parent_id: str, createPCommentInput: CreatePCommentInput) -> PComment:
        """
        댓글 생성
        --input
            - createPCommentInput: 댓글 생성 정보
        --output
            - PComment: 댓글 딕셔너리
        """
        db = get_db_session()

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
    
        # reply_id가 None인 경우 댓글 리스트를 가져옵니다.
        pcomment = db.query(PCommentTable).filter(
            PCommentTable.post_id == post_id,
            PCommentTable.deleteTime == None,
            PCommentTable.reply_id == None).all()
        
        # post가 없는 경우 CustomException을 발생시킵니다.
        if pcomment is None:
            raise CustomException("Post not found")
        
        return pcomment
        

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

        # Comment 중 reply_id가 comment_id인 경우를 찾아서 대댓글 리스트를 가져옵니다.
        pcomment = db.query(PCommentTable).filter(
            PCommentTable.reply_id == comment_id,
            PCommentTable.deleteTime == None).all()
        
        # 입력된 comment_id가 없는 경우 CustomException을 발생시킵니다.
        if pcomment is None:
            raise CustomException("Comment reply not found")

        return pcomment

        
    # 댓글 수정
    async def updatePComment(self, updatePCommentInput: UpdatePCommentInput, parent_id: str) -> Optional[PComment]:
        """
        댓글 수정
        --input
            - updatePCommentInput: 댓글 수정 정보
        --output
            - PComment: 댓글 딕셔너리
        """
        db = get_db_session()
        
        pcomment = db.query(PCommentTable).filter(
            PCommentTable.parent_id == parent_id,
            PCommentTable.comment_id == updatePCommentInput.comment_id,
            PCommentTable.deleteTime == None).first()
        
        # pcomment가 없는 경우 CustomException을 발생시킵니다.
        if pcomment is None:
            raise CustomException("Comment not found")

        pcomment.content = updatePCommentInput.content
        pcomment.modifyTime = datetime.now()

        db.add(pcomment)
        db.commit()
        db.refresh(pcomment)

        return pcomment


    # 댓글 삭제
    async def deletePComment(self, deletePCommentInput: DeletePCommentInput, parent_id: str) -> PComment:
        """
        댓글 삭제
        --input
            - deletePCommentInput: 댓글 삭제 정보
        --output
            - PComment: 댓글 딕셔너리
        """
        db = get_db_session()

        pcomment = db.query(PCommentTable).filter(
            PCommentTable.parent_id == parent_id,
            PCommentTable.comment_id == deletePCommentInput.comment_id,
            PCommentTable.deleteTime == None).first()
        
        # pcomment가 없는 경우 CustomException을 발생시킵니다.
        if pcomment is None:
            raise CustomException("Comment not found")

        # pcomment의 data를 삭제하지 않고 deleteTime을 추가하여 삭제된 것으로 표시합니다.
        setattr(pcomment, 'deleteTime', datetime.now())

        db.add(pcomment)
        db.commit()
        db.refresh(pcomment)

        return pcomment