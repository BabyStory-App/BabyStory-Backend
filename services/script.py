from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from model.pscript import ScriptTable
from schemas.script import *

from db import get_db_session

class ScriptService:

    # 스크립트 생성
    def createScript(self, createScriptInput: CreateScriptInput, parent_id: str) -> Optional[Script]:
        """
        스크립트 생성
        --input
            - createScriptInput.post_id: 게시물 아이디
            - createScriptInput.parent_id: 스크립트한 부모 아이디
        --output
            - Script: 스크립트 딕셔너리
        """
        db = get_db_session()
        try:
            script = ScriptTable(
                post_id=createScriptInput.post_id,
                parent_id=parent_id
            )

            db.add(script)
            db.commit()
            db.refresh(script)

            return script
        
        except Exception as e:
            db.rollback()
            raise (e)
        
    # 스크립트 삭제
    def deleteScript(self, deleteScriptInput: DeleteScriptInput, parent_id: str) -> Optional[Script]:
        """
        스크립트 삭제
        --input
            - deleteScriptInput.post_id: 게시물 아이디
            - deleteScriptInput.parent_id: 스크립트한 부모 아이디
        --output
            - Script: 스크립트 딕셔너리
        """
        db = get_db_session()
        try:
            script = db.query(ScriptTable).filter(
                ScriptTable.post_id == deleteScriptInput.post_id,
                ScriptTable.parent_id == parent_id
            ).first()

            if script is None:
                return None

            db.delete(script)
            return script
        
        except Exception as e:
            db.rollback()
            raise (e)