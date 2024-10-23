from pydantic import BaseModel
from typing import Optional, List

from model.aidoctorchat import *
from model.aidoctorroom import *


class NewAiChatInput(BaseModel):
    chatroom_id: Optional[int]
    ask: str


class NewAiChatOutput(BaseModel):
    room_id: int
    llm_prompt: str
    createTime: datetime
    chat: AIDoctorChat


class GetChatroomListOutput(BaseModel):
    status: int
    message: str
    chatrooms: List[AIDoctorRoom]


class LoadChatHistoryOutput(BaseModel):
    room_id: int
    createTime: datetime
    chatList: List[AIDoctorChat]


class LoadChatHistoryServiceOutput(BaseModel):
    roomCreateTime: datetime
    chat_history: List[AIDoctorChat]
