from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from model.pheart import PHeartTable
from schemas.pheart import *

from db import get_db_session

class PHeartService:

    # 하트 생성
    def createPHeart(self, createPHeartInput: CreatePHeartInput, parent_id: str) -> Optional[PHeart]:
        """
        하트 생성
        --input
            - createPHeartInput.post_id: 게시물 아이디
            - createPHeartInput.parent_id: 하트 누른 부모 아이디
        --output
            - PHeart: 하트 딕셔너리
        """
        db = get_db_session()
        try:
            pheart = PHeartTable(
                post_id=createPHeartInput.post_id,
                parent_id = parent_id,
                createTime = datetime.now()
            )

            db.add(pheart)
            db.commit()
            db.refresh(pheart)

            return pheart
        
        except Exception as e:
            db.rollback()
            raise (e)
        
    # 하트 삭제
    def deletePHeart(self, deletePHeartInput: DeletePHeartInput, parent_id: str) -> Optional[PHeart]:
        """
        하트 삭제
        --input
            - deletePHeartInput.post_id: 게시물 아이디
            - deletePHeartInput.parent_id: 하트 누른 부모 아이디
        --output
            - PHeart: 하트 딕셔너리
        """
        db = get_db_session()
        try:
            pheart = db.query(PHeartTable).filter(
                PHeartTable.post_id == deletePHeartInput.post_id,
                PHeartTable.parent_id == parent_id
            ).first()

            if pheart is None:
                return None

            db.delete(pheart)
            db.commit()

            return pheart

        except Exception as e:
            db.rollback()
            raise (e)