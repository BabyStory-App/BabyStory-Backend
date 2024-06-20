from typing import Optional, Union
from fastapi import HTTPException

from model.friend import FriendTable

from db import get_db_session


class FriendService:

    # 부모 생성
    def createFriend(self, parent_id: str,
                     friend: str) :
        db = get_db_session()
        try:
            friend = FriendTable(
                parent_id=parent_id,
                friend=friend
            )

            db.add(friend)
            db.commit()
            db.refresh(friend)

            return friend

        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to create friend")

    # # 부모 정보 조회
    # def getParent(self, parent_id: str) -> Optional[Parent]:
    #     db = get_db_session()
    #     try:
    #         parent = db.query(ParentTable).filter(
    #             ParentTable.parent_id == parent_id).first()

    #         return parent
        
    #     except Exception as e:
    #         print(e)
    #         raise HTTPException(
    #             status_code=400, detail="Failed to get parent")

    # # 부모 정보 수정
    # def updateParent(self, parent_id: str, 
    #                  updateParentInput: UpdateParentInput) -> Optional[Parent]:
    #     db = get_db_session()
    #     try:
    #         parent = db.query(ParentTable).filter(
    #             ParentTable.parent_id == parent_id).first()
            
    #         if parent is None:
    #             return False

    #         for key in updateParentInput.dict().keys():
    #             setattr(parent, key, updateParentInput.dict()[key])

    #         db.add(parent)
    #         db.commit()
    #         db.refresh(parent)

    #         return parent
        
    #     except Exception as e:
    #         db.rollback()
    #         print(e)
    #         raise HTTPException(
    #             status_code=400, detail="Failed to update parent")
        

    # # 부모 삭제
    # def deleteParent(self, parent_id: str) -> bool:
    #     db = get_db_session()
    #     try:
    #         parent = db.query(ParentTable).filter(
    #             ParentTable.parent_id == parent_id).first()
            
    #         if parent is None:
    #             return False

    #         db.delete(parent)
    #         db.commit()

    #         return True
    #     except Exception as e:
    #         db.rollback()
    #         print(e)
    #         raise HTTPException(
    #             status_code=400, detail="Failed to delete parent")

    # def getParentAll(self):
    #     db=get_db_session()
    #     try:
    #         parent = db.query(ParentTable).all()

    #         return parent
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=400, detail="Failed to get parent")

