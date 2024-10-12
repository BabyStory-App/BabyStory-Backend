from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from db import get_db_session

from model.pheart import PHeartTable
from schemas.pheart import *
from error.exception.customerror import *

class PHeartService:

    # 하트 관리
    def managePHeart(self, managePHeartInput: ManagePHeartInput, parent_id:str) -> ManagePHeartOutput:
        """
        하트 관리
        --input
            - managePHeartInput.post_id: 게시물 아이디
        --output
            - PHeart: 하트 딕셔너리
        """
        db = get_db_session()

        pheart = db.query(PHeartTable).filter(
            PHeartTable.post_id == managePHeartInput.post_id,
            PHeartTable.parent_id == parent_id
        ).first()

        if pheart is None:
            new_pheart = PHeartTable(
                post_id=managePHeartInput.post_id,
                parent_id = parent_id,
                createTime = datetime.now()
            )

            try:
                db.add(new_pheart)
                db.commit()
                db.refresh(new_pheart)
                return {'hasCreated': True, 'message': 'Success to create pheart', 'pheart': new_pheart}
            
            except Exception as e:
                db.rollback()
                raise e

        else:
            try:
                db.delete(pheart)
                db.commit()
                return {'hasCreated': False, 'message': 'Success to delete pheart', 'pheart': pheart}
            
            except Exception as e:
                db.rollback()
                raise e

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
    def deletePHeart(self, deletePHeartInput: DeletePHeartInput, parent_id: str) -> Optional[List[PHeart]]:
        """
        하트 삭제
        --input
            - deletePHeartInput.post_id: 게시물 아이디
            - deletePHeartInput.parent_id: 하트 누른 부모 아이디
        --output
            - PHeart: 하트 딕셔너리
        """
        db = get_db_session()

        if ',' not in deletePHeartInput.post_id:
            post_id = [int(deletePHeartInput.post_id)]
        else:
            post_id = [int(num.strip()) for num in deletePHeartInput.post_id.split(",")]

        phearts = []
        for i in post_id:
            pheart = db.query(PHeartTable).filter(
                PHeartTable.post_id == i,
                PHeartTable.parent_id == parent_id
            ).first()

            # pheart가 없을 경우 CustomException을 발생시킵니다.
            if pheart is None:
                raise CustomException("PHeart not found")

            db.delete(pheart)
            db.commit()

            phearts.append(pheart)

        return phearts