from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from db import get_db_session

from model.pscript import PScriptTable
from schemas.pscript import *
from error.exception.customerror import *



class PScriptService:

    # 스크립트 생성
    def createPScript(self, createPScriptInput: CreatePScriptInput, parent_id: str) -> Optional[PScript]:
        """
        스크립트 생성
        --input
            - createScriptInput.post_id: 게시물 아이디
            - createScriptInput.parent_id: 스크립트한 부모 아이디
        --output
            - Script: 스크립트 딕셔너리
        """
        db = get_db_session()

        pscript = PScriptTable(
            post_id=createPScriptInput.post_id,
            parent_id=parent_id,
            createTime=datetime.now()
        )

        db.add(pscript)
        db.commit()
        db.refresh(pscript)

        return pscript


        
    # 스크립트 삭제
    def deletePScript(self, deletePScriptInput: DeletePScriptInput, parent_id: str) -> Optional[PScript]:
        """
        스크립트 삭제
        --input
            - deletePScriptInput.post_id: 게시물 아이디
            - deletePScriptInput.parent_id: 스크립트한 부모 아이디
        --output
            - PScript: 스크립트 딕셔너리
        """
        db = get_db_session()

        pscript = db.query(PScriptTable).filter(
            PScriptTable.post_id == deletePScriptInput.post_id,
            PScriptTable.parent_id == parent_id
        ).first()

        if pscript is None:
            return None

        db.delete(pscript)
        db.commit()

        return pscript