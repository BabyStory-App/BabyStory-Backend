from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer
from typing import List

from services.chatroom import ChatRoomService
from schemas.chatroom import *
from error.exception.customerror import *


router = APIRouter(
    prefix="/chatroom",
    tags=["/chatroom"],
    responses={404: {"description": "Not found"}},
)

chatRoomService = ChatRoomService()

# 채팅방 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_chatroom(createChatRoomInput: CreateChatRoomInput, parent_id: str = Depends(JWTBearer()))-> CreateChatRoomOutput:
    '''
    채팅방 생성
    --input
        - name: 채팅방 이름
        - parent_id: 부모 아이디
    --output
        - chatroom: 채팅방
    '''
    try:
        chatroom = chatRoomService.createChatRoom(parent_id, createChatRoomInput.name)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create chatroom")
    
    return { 'chatroom': chatroom }

# 채팅방 목록 조회
@router.get("/list", dependencies=[Depends(JWTBearer())])
async def get_chatroom_list(parent_id: str = Depends(JWTBearer()))-> GetChatRoomListOutput:
    '''
    채팅방 목록 조회
    --input
        - parent_id: 부모 아이디
    --output
        - chatroom: 채팅방 목록
    '''
    try:
        chatroom = chatRoomService.getChatRoomList(parent_id)

    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get chatroom list")


    return { 'status': 'success 'if chatroom  else 'failed',
            'chatrooms': chatroom }

# 채팅방 초대
@router.post("/invite", dependencies=[Depends(JWTBearer())])
async def invite_chatroom(createInviteInput:CreateInviteInput, parent_id: str = Depends(JWTBearer())) -> CreateInviteOutput:
    '''
    채팅방 초대
    --input
        - invite_id: 초대할 아이디
        - room_id: 채팅방 아이디
        - parent_id: 부모 아이디
    --output
        - success: 성공 여부
    '''
    try:
        chatroom = chatRoomService.inviteChatRoom(createInviteInput.invite_id, createInviteInput.room_id, parent_id)
    
    except CustomException as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=e.message)
    
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to invite chatroom")
    
    return { 'success': 200 if chatroom else 403 }

# 채팅방 나가기
@router.post("/exit", dependencies=[Depends(JWTBearer())])
async def exit_chatroom(createExitInput: CreateExitInput, parent_id: str = Depends(JWTBearer()))->CreateExitOutput:
    '''
    채팅방 나가기
    --input
        - room_id: 채팅방 아이디
        - parent_id: 부모 아이디
    --output
        - success: 성공 여부
    '''
    try:
        chatroom = chatRoomService.exitChatRoom(createExitInput.room_id, parent_id)
    
    except CustomException as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=e.message)
    
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to exit chatroom")
    
    return { 'success': 200 if chatroom else 403 }

# 채팅방 수정
@router.post("/update", dependencies=[Depends(JWTBearer())])
async def update_chatroom(updateChatRoomInput:UpdateChatRoomInput, parent_id: str = Depends(JWTBearer()))->UpdateChatRoomOutput:
    '''
    채팅방 수정
    --input
        - room_id: 채팅방 아이디
        - name: 채팅방 이름
        - parent_id: 부모 아이디
    --output
        - success: 성공 여부
    '''
    try:
        chatroom = chatRoomService.updateChatRoom(updateChatRoomInput.room_id, updateChatRoomInput.name, parent_id)
    
    except CustomException as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=e.message)
    
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to update chatroom")
    
    return { 'success': 200 if chatroom else 403 }

# 채팅방 채팅 내용 조회
@router.get("/{chatroom_id}/{chat_id}", dependencies=[Depends(JWTBearer())])
async def get_chatroom_chat(chatroom_id: int, chat_id: str, parent_id: str = Depends(JWTBearer())):
    '''
    채팅방 채팅 내용 조회
    --input
        - chatroom_id: 채팅방 아이디
        - chat_id: 채팅 아이디
        - parent_id: 부모 아이디
    --output
        - chat: 채팅 내용
    '''
    try:
        chat = chatRoomService.getChat(chatroom_id, chat_id, parent_id)
    
    except CustomException as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=e.message)
    
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get chatroom chat")
    
    return { 'status': 'success' if chat else 'failed',
            "data": {
                "chatroom_id": chatroom_id,
                "chatList": chat
            }}


# 채팅방 조회
@router.get("/get", dependencies=[Depends(JWTBearer())])
async def get_chatroom(parent_id: str = Depends(JWTBearer())) -> GetChatRoomOutput:
    '''
    채팅방 조회
    --input
        - parent_id: 부모 아이디
    --output
        - chatroom: 채팅방 목록
    '''
    try:
        chatroom = chatRoomService.getChatRoom(parent_id)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get chatroom")
    
    return { 'chatroom': chatroom }