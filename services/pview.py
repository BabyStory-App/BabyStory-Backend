from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from model.pview import PViewTable
from schemas.pview import *

from db import get_db_session
from error.exception.customerror import *

class PViewService:
        
    # view 관리
    def managePView(self, managePViewInput: ManagePViewInput, parent_id:str) -> Optional[PView]:
        """
        view 관리
        --input
            - managePViewInput.post_id: 게시물 아이디
        --output
            - PView: 조회 딕셔너리
        """
        db = get_db_session()

        view = db.query(PViewTable).filter(
            PViewTable.post_id == managePViewInput.post_id,
            PViewTable.parent_id == parent_id
        ).first()

        if view is None:
            new_view = PViewTable(
                post_id=managePViewInput.post_id,
                parent_id = parent_id,
                createTime = datetime.now()
            )

            try:
                db.add(new_view)
                db.commit()
                db.refresh(new_view)
                return new_view
            
            except Exception as e:
                db.rollback()
                raise e

        else:
            try:
                db.delete(view)
                db.commit()
                return view
            
            except Exception as e:
                db.rollback()
                raise e
        
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

        post_id = [int(num.strip()) for num in deletePViewInput.post_id.split(",")]

        views = []
        for i in post_id:
            view = db.query(PViewTable).filter(
                    PViewTable.post_id == i,
                    PViewTable.parent_id == parent_id
                ).first()
    
            # pview가 없을 경우 CustomException을 발생시킵니다.
            if view is None:
                raise CustomException("PView not found")

            db.delete(view)
            db.commit()

            views.append(view)

        return views