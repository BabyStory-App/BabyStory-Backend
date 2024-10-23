from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from db import get_db_session

from model.chat import Chat, ChatTable
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
                name=name,
                memberCount=0
            )

            db.add(chatroom)
            db.commit()
            db.refresh(chatroom)

            return chatroom
        
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=400, detail="Failed to create chatroom")
    

    # 채팅방 목록 조회
    def getChatRoomList(self, parent_id: str) -> List[ChatRoom]:
        """
        채팅방 목록 조회
        --input
            - parent_id: 부모 아이디
        --output
            - ChatRoom: 채팅방 목록
        """
        db = get_db_session()

        # 부모 아이디로 부모가 속한 채팅방 조회
        chatroom = db.query(PCConnectTable).filter(PCConnectTable.parent_id == parent_id).all()
        # room_id만 가져오기
        room_ids = [c.room_id for c in chatroom]

        # 각 room_id에 해당하는 채팅방 정보 조회
        chatroom = db.query(ChatRoomTable).filter(ChatRoomTable.room_id.in_(room_ids)).all()

        # 각 room_id에 해당하는 채팅방의 chattable의 count로 개수 세기
        for c in chatroom:
            chat_count = db.query(ChatTable).filter(ChatTable.room_id == c.room_id).count()
            c.chatCount = chat_count

        return chatroom


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
            raise CustomException("You do not have access to the chat room.")
        
        # 이미 초대된 아이디인지 확인
        if db.query(PCConnectTable).filter(PCConnectTable.room_id == room_id,
                                            PCConnectTable.parent_id == invite_id).first():
            raise CustomException("User already in chatroom.")

        # 채팅방에 초대할 아이디 추가
        try:
            pcconnect = PCConnectTable(
                parent_id=invite_id,
                room_id=room_id
            )

            db.add(pcconnect)

            # 채팅방의 memberCount 증가
            chatroom = db.query(ChatRoomTable).filter(ChatRoomTable.room_id == room_id).first()
            if chatroom:
                chatroom.memberCount += 1

            db.commit()
            db.refresh(pcconnect)

            return pcconnect
        
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Failed to invite chatroom")
        

    # 채팅방 나가기
    def exitChatRoom(self,  room_id: int, parent_id: str) -> bool:
        """
        채팅방 나가기
        --input
            - parent_id: 부모 아이디
            - room_id: 채팅방 아이디
        --output
            - success: 성공 여부
        """
        db = get_db_session()

        # 채팅방이 있는지 확인
        if db.query(ChatRoomTable).filter(ChatRoomTable.room_id == room_id).first() is None:
            raise CustomException("Chatroom not found.")

        # 채팅방에 속한 부모 목록 조회
        pcconnect = db.query(PCConnectTable).filter(PCConnectTable.room_id == room_id).all()
        parent_ids = [p.parent_id for p in pcconnect]

        # 부모가 채팅방에 속해있는지 확인
        if parent_id not in parent_ids:
            raise CustomException("Not a chatroom members")

        # 채팅방 나가기
        try:
            db.query(PCConnectTable).filter(PCConnectTable.room_id == room_id, 
                                            PCConnectTable.parent_id == parent_id).delete()
            # 채팅방의 memberCount 감소
            chatroom = db.query(ChatRoomTable).filter(ChatRoomTable.room_id == room_id).first()
            
            if chatroom and chatroom.memberCount > 0:
                chatroom.memberCount -= 1
            
            db.commit()

            return True
        
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Failed to leave chatroom")
        

    # 채팅방 수정
    def updateChatRoom(self, room_id: str, name: str, parent_id: str) -> ChatRoom:
        """
        채팅방 수정
        --input
            - room_id: 채팅방 아이디
            - name: 채팅방 이름
            - parent_id: 부모 아이디
        --output
            - chatroom: 채팅방 정보
        """
        db = get_db_session()

        # parent_id가 방장인지 확인
        if db.query(ChatRoomTable).filter(
            ChatRoomTable.room_id == room_id).first().parent_id != parent_id:
            raise CustomException("Not authorized to change chatroom information.")

        # 채팅방 정보 조회
        chatroom = db.query(ChatRoomTable).filter(ChatRoomTable.room_id == room_id).first()

        # 채팅방 이름 수정
        chatroom.name = name

        try:
            db.commit()
            db.refresh(chatroom)

            return chatroom
        
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Failed to update chatroom")
        

    # 채팅 내용 가져오기
    def getChat(self, room_id: int, chat_id: str ,parent_id: str) -> List[Chat]:
        """
        채팅 내용 가져오기
        --input
            - room_id: 채팅방 아이디
            - parent_id: 부모 아이디
            - chat_id: 채팅 아이디
        --output
            - chat: 채팅 내용
        """
        db = get_db_session()

        # 채팅방에 속한 부모 목록 조회
        pcconnect = db.query(PCConnectTable).filter(PCConnectTable.room_id == room_id).all()
        parent_ids = [p.parent_id for p in pcconnect]

        # 부모가 채팅방에 속해있는지 확인
        if parent_id not in parent_ids:
            raise CustomException("Not authorized to get chat list from {chatroom_id}r")
        
        # chat_id가 unknown인 경우 최근 20개의 채팅 내용 조회
        if chat_id == "unknown":
            chat = db.query(ChatTable).filter(ChatTable.room_id == room_id
                                            ).order_by(ChatTable.chat_id.desc()).limit(20).all()
            
            return chat
        
        # 만약 chat_id가 숫자형식이 아닌 경우
        elif not chat_id.isdigit():
            raise CustomException("Invalid chat_id")
        
        else:
            # chat_id 이전 20개의 채팅 내용 조회
            chat = db.query(ChatTable).filter(ChatTable.room_id == room_id, ChatTable.chat_id < chat_id
                                            ).order_by(ChatTable.chat_id.desc()).limit(20).all()

        return chat

    
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