from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from db import get_db_session

from model.pcomment import PCommentTable, PComment
from model.parent import ParentTable
from schemas.pcomment import *
from error.exception.customerror import *


class PCommentService:

    # 댓글 생성
    def createPComment(self, parent_id: str, createPCommentInput: CreatePCommentInput) -> PComment:
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
    def getAllPComment(self, post_id: int) -> List[CommentOutput]:
        """
        모든 댓글 가져오기
        --input
            - post_id: 게시물 아이디
        --output
            - List[PComment]: 댓글 리스트
        """
        db = get_db_session()

        # Comments를 가져오면서 ParentTable의 parent_id, nickname, photoId도 함께 가져오기
        pcomments = db.query(
            PCommentTable.comment_id,
            PCommentTable.content,
            PCommentTable.createTime,
            PCommentTable.modifyTime,
            PCommentTable.cheart,
            PCommentTable.reply_id,
            ParentTable.parent_id,
            ParentTable.nickname,
            ParentTable.photoId
        ).join(ParentTable, PCommentTable.parent_id == ParentTable.parent_id).filter(
            PCommentTable.post_id == post_id,
            PCommentTable.deleteTime == None
        ).all()

        comments = []
        reply_comments = {}
        for i in range(len(pcomments)):
            comment_data = {
                'comment_id': pcomments[i][0],
                'content': pcomments[i][1],
                'createTime': pcomments[i][2],
                'modifyTime': pcomments[i][3],
                'cheart': pcomments[i][4],
                'parent': {
                    'parent_id': pcomments[i][6],
                    'nickname': pcomments[i][7],
                    'photoId': pcomments[i][8]
                },
                'replies': None
            }
            if pcomments[i][5] == None:
                comments.append(comment_data)
            else:
                if pcomments[i][5] not in reply_comments:
                    reply_comments[pcomments[i][5]] = []
                reply_comments[pcomments[i][5]].append(comment_data)

        # 댓글에 대댓글이 있는 경우 대댓글을 댓글에 추가.
        for i in range(len(comments)):
            if comments[i]['comment_id'] in reply_comments:
                comments[i]['replies'] = reply_comments[comments[i]['comment_id']]

        comments.sort(key=lambda x: x['createTime'], reverse=True)

        return comments


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

        pcomment = db.query(PCommentTable).filter(
            PCommentTable.reply_id == comment_id,
            PCommentTable.deleteTime == None).all()

        # 입력된 comment_id가 없는 경우 CustomException을 발생시킵니다.
        if pcomment is None:
            raise CustomException("Comment reply not found")

        pcomments = []
        pcomments = db.query(PCommentTable).filter(
            PCommentTable.reply_id == comment_id,
            PCommentTable.deleteTime == None).all()

        return pcomments


    # 댓글 수정
    async def updatePComment(self, updatePCommentInput: UpdatePCommentInput, parent_id: str) -> Optional[PComment]:
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
            - deletePCommentInput.comment_id: 댓글 아이디
            - deletePCommentInput.deleteTime: 댓글 삭제 시간
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
