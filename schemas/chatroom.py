from pydantic import BaseModel
from typing import Optional, List

from model.chatroom import ChatRoom


class CreateChatRoomOutput(BaseModel):
    chatroom: Optional[ChatRoom]

class CreateInviteOutput(BaseModel):
    success: int

class GetChatRoomOutput(BaseModel):
    chatroom: List[ChatRoom]

