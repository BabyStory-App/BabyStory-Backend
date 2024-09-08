from typing import Optional
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from model.cheart import CHeartTable
from schemas.cheart import *
from db import get_db_session
from error.exception.customerror import *

class CHeartService:

    # 하트 생성
    def createCHeart(self,
                    createCHeartInput: CreateCHeartInput,
                    parent_id: str) -> Optional[CHeart]:
        """
        하트 생성
        --input
            - createCHeartInput: 댓글 하트 생성 정보
        --output
            - CHeart: 하트 딕셔너리
        """
        db = get_db_session()

        Cheart = CHeartTable(
            comment_id=createCHeartInput.comment_id,
            parent_id = parent_id,
            createTime = datetime.now()
        )
        db.add(Cheart)
        db.commit()
        db.refresh(Cheart)

        return Cheart

        
    # 하트 삭제
    def deleteCHeart(self, deleteCHeartInput: DeleteCHeartInput, parent_id: str) -> Optional[CHeart]:
        """
        하트 삭제
        --input
            - deleteCHeartInput: 댓글 하트 삭제 정보
        --output
            - CHeart: 하트 딕셔너리
        """
        db = get_db_session()

        Cheart = db.query(CHeartTable).filter(
            CHeartTable.comment_id == deleteCHeartInput.comment_id,
            CHeartTable.parent_id == parent_id
        ).first()
        db.delete(Cheart)
        db.commit()

        if Cheart is None:
            raise CustomException("CHeart not found")
        
        return Cheart