from typing import Optional, Union
from fastapi import HTTPException

from model.friend import FriendTable
from schemas.friend import *

from db import get_db_session
from error.exception.customerror import *


class FriendService:

    # 친구 관계 관리
    def manageFriend(self, manageFriendInput: ManageFriendInput,
                     parent_id: str) -> ManageFriendOutput:
        """
        친구 관계 관리
        --input
            - manageFriendInput.friend: 친구 아이디
        --output
            - Friend: 친구 딕셔너리
        """
        db = get_db_session()

        friend = db.query(FriendTable).filter(
            FriendTable.parent_id == parent_id,
            FriendTable.friend == manageFriendInput.friend
        ).first()

        if friend is None:
            new_friend = FriendTable(
                parent_id=parent_id,
                friend=manageFriendInput.friend
            )

            try:
                db.add(new_friend)
                db.commit()
                db.refresh(new_friend)
                return {'hasCreated': True, 'message': 'Success to create friend', 'friend': new_friend}
            
            except Exception as e:
                db.rollback()
                raise e
            
        else:
            try:
                db.delete(friend)
                db.commit()
                return {'hasCreated': False, 'message': 'Success to delete friend', 'friend': friend}
            
            except Exception as e:
                db.rollback()


    # 친구 관계 생성
    def createFriend(self, createFriendInput: CreateFriendInput,
                     parent_id: str) -> Optional[Friend]:
        db = get_db_session()
        try:
            friend = FriendTable(
                parent_id=parent_id,
                friend=createFriendInput.friend
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
        
        
    # 친구 관계 삭제
    def deleteFriend(self, deleteFriendInput: DeleteFriendInput,
                     parent_id: str) -> Optional[list[Friend]]:
        """
        친구 관계 삭제
        --input
            - deleteFriendInput.friend: 친구 아이디
        --output
            - Friend: 친구 딕셔너리
        """
        db = get_db_session()

        if ',' not in deleteFriendInput.friend:
            friend = [str(deleteFriendInput.friend)]
        else:
            friend = [friend.strip() for friend in deleteFriendInput.friend.split(',')]  # 쉼표로 나누어 리스트 생성

        friends = []
        for i in friend:
            parent = db.query(FriendTable).filter(
                FriendTable.parent_id == parent_id,
                FriendTable.friend == i
            ).first()

            if parent is None:
                raise CustomException("Friend not found")
            
            db.delete(parent)
            db.commit()

            friends.append(parent)

        return friends