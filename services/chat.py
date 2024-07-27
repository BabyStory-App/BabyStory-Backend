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
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.client_info: Dict[WebSocket, str] = {}  # Maps WebSocket to unique client IDs

    async def connect(self, room_id: int, websocket: WebSocket, client_id: str):

        db=get_db_session()

        # 실제 존재하는 client_id인지 확인
        if db.query(ParentTable).filter(ParentTable.parent_id == client_id).first() is None:
            raise CustomException("Not available parent")
        
        # 채팅방에 연결되어 있는지 확인
        if db.query(PCConnectTable).filter(PCConnectTable.room_id == room_id).filter(PCConnectTable.parent_id == client_id).first() is None:
            raise CustomException("Not Authorized to connect to this room")
        
        # client_id 중복 확인
        if client_id in self.client_info.values():
            raise CustomException("Client ID already exists")
        
        await websocket.accept()

        self.active_connections.setdefault(room_id, []).append(websocket)
        self.client_info[websocket] = client_id
        print(f"User {client_id} connected to room {room_id}. Current connections: {len(self.active_connections[room_id])}")
        print(f"Room Member connections: {self.active_connections[room_id]}")

    def disconnect(self, room_id: int, websocket: WebSocket):
        if room_id in self.active_connections and websocket in self.active_connections[room_id]:
            self.active_connections[room_id].remove(websocket)
            del self.client_info[websocket]
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
            print(f"User disconnected from room {room_id}. Current connections: {len(self.active_connections.get(room_id, []))}")
            #print(f"Active connections: {self.active_connections}")
            print(f"Room Member connections: {self.active_connections[room_id]}")

    async def broadcast(self, room_id: int, client_id: str, data: str):
        db=get_db_session()

        nickname=db.query(ParentTable.nickname).filter(ParentTable.parent_id==client_id).first()

        # nickname_tuple이 None일 수 있으므로 체크 필요
        if nickname:
            nickname = nickname[0]
        else:
            CustomException("Nickname not found")

        message_data = json.loads(data)
        chatType = message_data.get("type")
        content = message_data.get("content")
        createTime = datetime.now()

        # chat db에 저장
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
        
        

        connections = self.active_connections.get(room_id, [])

        for connection in connections:
            try:
                await connection.send_text(f"type: {chatType}, {nickname}: {content} ({createTime})")
            except Exception as e:
                print(f"Error sending message: {e}")

    def get_room_status(self, room_id: int):
        connections = self.active_connections.get(room_id, [])
        client_ids = [self.client_info.get(conn, "Unknown") for conn in connections]
        return f"Total clients: {len(connections)}\nClients: {', '.join(client_ids)}"