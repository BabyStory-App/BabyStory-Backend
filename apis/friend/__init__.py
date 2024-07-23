from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Header
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer

from services.friend import FriendService
from schemas.friend import *

router = APIRouter(
    prefix="/friend",
    tags=["friend"],
    responses={404: {"description": "Not found"}},
)

friendService = FriendService()

# 친구관계 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_post(friend: CreateFriendInput,
                parent_id: str = Depends(JWTBearer())):
    
    # 부모 아이디가 없으면 에러
    if parent_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")

    friend = friendService.createFriend(parent_id, friend.friend)

    if friend is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Friend not found")
    
    return { 'friend': friend }
