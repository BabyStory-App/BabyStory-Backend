from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session

from model.share import ShareTable
from schemas.share import *

from db import get_db_session

class ShareService:
    
    # 공유 생성
    def createShare(self, createShareInput: CreateShareInput, parent_id: str) -> Optional[Share]:
        """
        공유 생성
        --input
            - createShareInput.post_id: 게시물 아이디
            - createShareInput.parent_id: 공유한 부모 아이디
        --output
            - Share: 공유 딕셔너리
        """
        db = get_db_session()
        try:
            share = ShareTable(
                post_id=createShareInput.post_id,
                parent_id=parent_id
            )

            db.add(share)
            db.commit()
            db.refresh(share)

            return share
        
        except Exception as e:
            db.rollback()
            raise (e)
        
    # 공유 삭제
    def deleteShare(self, deleteShareInput: DeleteShareInput, parent_id: str) -> Optional[Share]:
        """
        공유 삭제
        --input
            - deleteShareInput.post_id: 게시물 아이디
            - deleteShareInput.parent_id: 공유한 부모 아이디
        --output
            - Share: 공유 딕셔너리
        """
        db = get_db_session()
        try:
            share = db.query(ShareTable).filter(
                ShareTable.post_id == deleteShareInput.post_id,
                ShareTable.parent_id == parent_id
            ).first()

            if share is None:
                return None

            db.delete(share)
            db.commit()

            return share
        
        except Exception as e:
            db.rollback()
            raise (e)