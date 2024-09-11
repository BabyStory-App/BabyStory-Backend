from pydantic import BaseModel
from typing import Optional, List

from model.chatroom import ChatRoom
from model.chat import Chat

class CreateChatRoomInput(BaseModel):
    name: str

class CreateChatRoomOutput(BaseModel):
    chatroom: Optional[ChatRoom]

class GetChatRoomListOutput(BaseModel):
    status: str
    chatrooms: List[ChatRoom]

class CreateInviteInput(BaseModel):
    invite_id: str
    room_id: str

class CreateInviteOutput(BaseModel):
    success: int

class CreateExitInput(BaseModel):
    room_id: str

class CreateExitOutput(BaseModel):
    success: int

class UpdateChatRoomInput(BaseModel):
    room_id: str
    name: str

class UpdateChatRoomOutput(BaseModel):
    success: int

class GetChatRoomChatInput(BaseModel):
    chatroom_id: int
    chat_id: str

class GetChatRoomChatOutputData(BaseModel):
    chatroom_id: int
    chatList: List[Chat]

class GetChatRoomChatOutput(BaseModel):
    status: str
    data: GetChatRoomChatOutputData

class GetChatRoomOutput(BaseModel):
    chatroom: List[ChatRoom]

