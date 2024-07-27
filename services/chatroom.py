from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from db import get_db_session

from model.chatroom import ChatRoom, ChatRoomTable
from model.pcconnect import PCConnectTable
from model.parent import ParentTable
from schemas.chatroom import *
from error.exception.customerror import *

class ChatRoomService:
    # 채팅방 생성
    def createChatRoom(self, parent_id: str, name: str) -> ChatRoom:
        """
        댓글 생성
        --input
            - parent_id: 부모 아이디
            - name: 채팅방이름
        --output
            - ChatRoom: 채팅방 정보
        """
        db = get_db_session()

        try:
            chatroom = ChatRoomTable(
                parent_id=parent_id,
                lastChat=1,
                name=name
            )

            db.add(chatroom)
            db.commit()
            db.refresh(chatroom)

            return chatroom
        
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=400, detail="Failed to create chatroom")
    
    

    # 채팅방 초대
    def inviteChatRoom(self, invite_id: str, room_id: str, parent_id: str) -> PCConnectTable:
        """
        채팅방 초대
        --input
            - invite_id: 초대할 아이디
            - room_id: 채팅방 아이디
            - parent_id: 부모 아이디
        --output
            - success: 성공 여부
        """
        db = get_db_session()

        # 초대할 아이디가 부모인지 확인
        if db.query(ParentTable).filter(ParentTable.parent_id == invite_id).first() is None:
            raise CustomException("Not available parent")
        
        # 초대할 채팅방이 있는지 확인
        if db.query(ChatRoomTable).filter(ChatRoomTable.room_id == room_id).first() is None:
            raise CustomException("Not exist chatroom")

        # 채팅방 소유자인지 확인
        if db.query(ChatRoomTable).filter(
            ChatRoomTable.room_id == room_id).first().parent_id != parent_id:
            raise CustomException("Not a owner")

        # 채팅방에 초대할 아이디 추가
        try:
            pcconnect = PCConnectTable(
                parent_id=invite_id,
                room_id=room_id
            )

            db.add(pcconnect)
            db.commit()
            db.refresh(pcconnect)

            return pcconnect
        
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Failed to invite chatroom")

    
    # 채팅방 조회
    def getChatRoom(self, parent_id: str) -> List[ChatRoom]:
        """
        채팅방 조회
        --input
            - parent_id: 부모 아이디
        --output
            - chatroom: 채팅방 목록
        """
        db = get_db_session()

        # 부모 아이디로 부모가 속한 채팅방 조회
        chatroom = db.query(PCConnectTable).filter(PCConnectTable.parent_id == parent_id).all()

        #room_id만 가져오기
        room_ids = [c.room_id for c in chatroom]

        #채팅방 목록 조회
        chatroom = db.query(ChatRoomTable).filter(ChatRoomTable.room_id.in_(room_ids)).all()
        

        return chatroom