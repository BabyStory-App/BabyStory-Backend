from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer

from services.pheart import PHeartService
from schemas.pheart import *

router = APIRouter(
    prefix="/pheart",
    tags=["pheart"],
    responses={404: {"description": "Not found"}},
)

pheartService = PHeartService()

# 하트 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_heart(createPHeartInput: CreatePHeartInput, 
                        parent_id: str = Depends(JWTBearer()))-> PHeart:
    """
    하트 생성
    --input
        - createPHeartInput.post_id: 게시물 아이디
        - parent_id: 하트 누른 부모 아이디
    --output
        - PHeart: 하트 딕셔너리
    """

    # 하트 생성
    result = pheartService.createPHeart(createPHeartInput, parent_id)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create pheart")

    return result

# 하트 삭제
@router.delete("/delete", dependencies=[Depends(JWTBearer())])
async def delete_heart(deletePHeartInput: DeletePHeartInput, 
                        parent_id: str = Depends(JWTBearer()))-> PHeart:
    """
    하트 삭제
    --input
        - deletePHeartInput.post_id: 게시물 아이디
        - parent_id: 하트 누른 부모 아이디
    --output
        - PHeart: 하트 딕셔너리
    """

    # 하트 삭제
    result = pheartService.deletePHeart(deletePHeartInput, parent_id)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete pheart")

    return result