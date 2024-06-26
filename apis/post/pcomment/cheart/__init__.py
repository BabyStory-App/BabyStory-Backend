from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer

from services.cheart import CHeartService
from schemas.cheart import *

router = APIRouter(
    prefix="/cheart",
    tags=["cheart"],
    responses={404: {"description": "Not found"}},
)

cheartService = CHeartService()

# 하트 생성
@router.post("/pheartCreate", dependencies=[Depends(JWTBearer())])
async def create_heart(createCHeartInput: CreateCHeartInput, 
                        parent_id: str = Depends(JWTBearer()))-> CHeart:
    """
    하트 생성
    --input
        - createCHeartInput.comment_id: 게시물 아이디
        - parent_id: 하트 누른 부모 아이디
    --output
        - CHeart: 하트 딕셔너리
    """

    # 하트 생성
    result = cheartService.createCHeart(createCHeartInput, parent_id)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="createheart not found")

    return result

# 하트 삭제
@router.delete("/CheartDelete", dependencies=[Depends(JWTBearer())])
async def delete_heart(deleteCHeartInput: DeleteCHeartInput, 
                        parent_id: str = Depends(JWTBearer()))-> CHeart:
    """
    하트 삭제
    --input
        - deleteCHeartInput.comment_id: 게시물 아이디
        - parent_id: 하트 누른 부모 아이디
    --output
        - CHeart: 하트 딕셔너리
    """

    # 하트 삭제
    result = cheartService.deleteCHeart(deleteCHeartInput, parent_id)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="deleteheart not found")

    return result