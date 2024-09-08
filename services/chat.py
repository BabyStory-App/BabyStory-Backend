from fastapi import HTTPException, WebSocket
from typing import Optional, List, Set, Dict
import json
from datetime import datetime

from db import get_db_session
from model.chatroom import ChatRoom, ChatRoomTable
from model.chat import ChatTable
from model.pcconnect import PCConnectTable
from model.parent import ParentTable

from schemas.chatroom import *
from error.exception.customerror import *

class ChatService:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}  # {parent_id: websocket}
        self.client_info: Dict[WebSocket, str] = {}  # Maps WebSocket to unique client IDs

    async def connect(self, websocket: WebSocket, client_id: str):
        db = get_db_session()

        # 실제 존재하는 client_id인지 확인
        if db.query(ParentTable).filter(ParentTable.parent_id == client_id).first() is None:
            raise CustomException("Not available parent")

        # client_id 중복 확인
        if client_id in self.active_connections:
            raise CustomException("Client ID already exists")
        
        await websocket.accept()

        # parent_id와 websocket 연결
        self.active_connections[client_id] = websocket
        self.client_info[websocket] = client_id

        print(f"User {client_id} connected. Total connections: {len(self.active_connections)}")

    async def disconnect(self, websocket: WebSocket):
        client_id = self.client_info.pop(websocket, None)

        if client_id:
            self.active_connections.pop(client_id, None)
            print(f"User {client_id} disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, client_id: str, data: str):
        db = get_db_session()

        # json형식인 data에서 room_id 추출
        room_id = json.loads(data).get("room_id")

        # 해당 room_id에 속한 모든 parent_id를 가져옴
        parent_ids = db.query(PCConnectTable.parent_id).filter(PCConnectTable.room_id == room_id).all()

        # 현재 사용자의 nickname을 가져옴
        nickname = db.query(ParentTable.nickname).filter(ParentTable.parent_id == client_id).first()

        if nickname:
            nickname = nickname[0]
        else:
            raise CustomException("Nickname not found")

        # 메시지 데이터 추출
        message_data = json.loads(data)
        chatType = message_data.get("type")
        content = message_data.get("content")
        createTime = datetime.now()

        # chat 데이터를 DB에 저장
        try:
            chat = ChatTable(
                parent_id=client_id,
                room_id=room_id,
                createTime=createTime,
                chatType=chatType,
                content=content
            )

            db.add(chat)
            db.commit()
            db.refresh(chat)

        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=400, detail="Failed to save chat data")

        # 해당 room_id에 속한 모든 parent_id에게 메시지 전송
        for parent_id_tuple in parent_ids:
            parent_id = parent_id_tuple[0]  # 튜플에서 실제 parent_id 값 추출
            websocket = self.active_connections.get(parent_id)
            if websocket:
                try:
                    await websocket.send_text(f"type: {chatType}, {nickname}: {content} ({createTime})")
                except Exception as e:
                    print(f"Error sending message: {e}")

    def get_room_status(self, parent_id: str):
        # parent_id를 key로 하는 websocket이 존재하는지 확인
        connections = [self.active_connections.get(parent_id)]
        client_ids = [self.client_info.get(conn, "Unknown") for conn in connections]
        return f"{self.active_connections},{self.client_info}Total clients: {len(connections)}\nClients: {', '.join(client_ids)}"
