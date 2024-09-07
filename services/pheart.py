from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from db import get_db_session

from model.pheart import PHeartTable
from schemas.pheart import *
from error.exception.customerror import *

class PHeartService:

    # 하트 생성
    def createPHeart(self, createPHeartInput: CreatePHeartInput, parent_id: str) -> Optional[PHeart]:
        """
        하트 생성
        --input
            - createPHeartInput: 게시물 하트 생성 정보
        --output
            - PHeart: 하트 딕셔너리
        """
        db = get_db_session()

        pheart = PHeartTable(
            post_id=createPHeartInput.post_id,
            parent_id = parent_id,
            createTime = datetime.now()
        )

        db.add(pheart)
        db.commit()
        db.refresh(pheart)

        return pheart


        
    # 하트 삭제
    def deletePHeart(self, deletePHeartInput: DeletePHeartInput, parent_id: str) -> Optional[PHeart]:
        """
        하트 삭제
        --input
            - deletePHeartInput: 게시물 하트 삭제 정보
        --output
            - PHeart: 하트 딕셔너리
        """
        db = get_db_session()

        pheart = db.query(PHeartTable).filter(
            PHeartTable.post_id == deletePHeartInput.post_id,
            PHeartTable.parent_id == parent_id
        ).first()
        db.delete(pheart)
        db.commit()

        # pheart가 없을 경우 CustomException을 발생시킵니다.
        if pheart is None:
            raise CustomException("PHeart not found")

        return pheart