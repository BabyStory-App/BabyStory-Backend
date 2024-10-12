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

# 친구관계 관리
@router.post("/", dependencies=[Depends(JWTBearer())])
async def manage_friend(manageFriendInput: ManageFriendInput,
                        parent_id: str = Depends(JWTBearer()))-> ManageFriendOutput:
    try:
        result = friendService.manageFriend(manageFriendInput, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to manage friend")
    return {"hasCreated": result['hasCreated'], "message": result['message'], "friend": result['friend']}

# 친구관계 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_post(createFriendInput: CreateFriendInput,
                parent_id: str = Depends(JWTBearer())) -> CreateFriendOutput:
    
    # 부모 아이디가 없으면 에러
    if parent_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")

    friend = friendService.createFriend(createFriendInput, parent_id)

    if friend is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Friend not found")
    
    return {"success": 200, "message": "Success to create friend", "friend": friend}


# 친구관계 삭제
@router.delete("/delete", dependencies=[Depends(JWTBearer())])
async def delete_post(deleteFriendInput: DeleteFriendInput,
                parent_id: str = Depends(JWTBearer())) -> DeleteFriendOutput:
    
    friend = friendService.deleteFriend(deleteFriendInput, parent_id)
    
    if friend is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Friend not found")
    return { "success": 200, "message": "Success to delete friend", "friend": friend }