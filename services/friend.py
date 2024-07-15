from typing import Optional, Union
from fastapi import HTTPException

from model.friend import FriendTable

from db import get_db_session


class FriendService:

    # 친구 관계 생성
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
