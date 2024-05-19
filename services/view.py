from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from model.view import ViewTable
from schemas.view import *

from db import get_db_session

class ViewService:
        
        # 조회 생성
        def createView(self, createViewInput: CreateViewInput, parent_id: str) -> Optional[View]:
            """
            조회 생성
            --input
                - createViewInput.post_id: 게시물 아이디
                - createViewInput.parent_id: 조회한 부모 아이디
            --output
                - View: 조회 딕셔너리
            """
            db = get_db_session()
            try:
                view = ViewTable(
                    post_id=createViewInput.post_id,
                    parent_id=parent_id
                )
    
                db.add(view)
                db.commit()
                db.refresh(view)
    
                return view
            
            except Exception as e:
                db.rollback()
                raise (e)
            
        # 조회 삭제
        def deleteView(self, deleteViewInput: DeleteViewInput, parent_id: str) -> Optional[View]:
            """
            조회 삭제
            --input
                - deleteViewInput.post_id: 게시물 아이디
                - deleteViewInput.parent_id: 조회한 부모 아이디
            --output
                - View: 조회 딕셔너리
            """
            db = get_db_session()
            try:
                view = db.query(ViewTable).filter(
                    ViewTable.post_id == deleteViewInput.post_id,
                    ViewTable.parent_id == parent_id
                ).first()
    
                if view is None:
                    return None
    
                db.delete(view)
                db.commit()

                return view
            
            except Exception as e:
                db.rollback()
                raise (e)