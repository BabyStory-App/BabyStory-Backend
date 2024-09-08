from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from model.pview import PViewTable
from schemas.pview import *

from db import get_db_session
from error.exception.customerror import *

class PViewService:
        
        # view 생성
        def createPView(self, createPViewInput: CreatePViewInput, parent_id: str) -> Optional[PView]:
            """
            view 생성
            --input
                - createPViewInput.post_id: 게시물 아이디
                - createPViewInput.parent_id: 조회한 부모 아이디
            --output
                - View: 조회 딕셔너리
            """
            db = get_db_session()

            view = PViewTable(
                    post_id=createPViewInput.post_id,
                    parent_id=parent_id,
                    createTime = datetime.now()
                )
            db.add(view)
            db.commit()
            db.refresh(view)
    
            return view

            
        # 조회 삭제
        def deletePView(self, deletePViewInput: DeletePViewInput, parent_id: str) -> Optional[PView]:
            """
            조회 삭제
            --input
                - deletePViewInput.post_id: 게시물 아이디
                - deletePViewInput.parent_id: 조회한 부모 아이디
            --output
                - View: 조회 딕셔너리
            """
            db = get_db_session()

            view = db.query(PViewTable).filter(
                    PViewTable.post_id == deletePViewInput.post_id,
                    PViewTable.parent_id == parent_id
                ).first()
            db.delete(view)
            db.commit()
            
            # pview가 없을 경우 CustomException을 발생시킵니다.
            if view is None:
                raise CustomException("PView not found")

            return view