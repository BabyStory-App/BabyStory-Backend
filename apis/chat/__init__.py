from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer
from typing import List, Optional, Dict
from fastapi import Query
import json

from services.chat import ChatService
# from services.postmain import PostMainService
# from schemas.search import *
# from schemas.postmain import *
from error.exception.customerror import *


router = APIRouter(
    prefix="/chat",
    tags=["/chat"],
    responses={404: {"description": "Not found"}},
)

chat_service = ChatService()

@router.websocket("/ws/{parent_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    parent_id: str
):
    
    client_id = parent_id
    
    try:
        await chat_service.connect(websocket, client_id)
        await websocket.send_text("connected")
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)
            #print(f"Received message: {data}")

            # data의 type이 status_request인 경우
            if json_data.get("type") == "status_request":
                status = chat_service.get_room_status(parent_id)
                await websocket.send_text(status)
                print(f"Sending status: {status}")
            else:
                await chat_service.broadcast(client_id, json.dumps(json_data))

    except CustomException as e:
        chat_service.disconnect(websocket)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=e.message)
    
    except WebSocketDisconnect:
        chat_service.disconnect(websocket)