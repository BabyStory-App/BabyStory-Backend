from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer
from error.exception.customerror import *

from services.cheart import CHeartService
from schemas.cheart import *

router = APIRouter(
    prefix="/cheart",
    tags=["cheart"],
    responses={404: {"description": "Not found"}},
)

cheartService = CHeartService()

# 댓글 하트 관리
@router.post("/", dependencies=[Depends(JWTBearer())])
async def manage_heart(manageCHeartInput: ManageCHeartInput,
                        parent_id: str = Depends(JWTBearer()))-> CHeart:
    try:
        result = cheartService.manageCHeart(manageCHeartInput, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to manage cheart")
    return result

# 댓글 하트 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_heart(createCHeartInput: CreateCHeartInput, 
                        parent_id: str = Depends(JWTBearer()))-> CHeart:
    try:
        result = cheartService.createCHeart(createCHeartInput, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create cheart")
    return result

# 댓글 하트 삭제
@router.delete("/delete", dependencies=[Depends(JWTBearer())])
async def delete_heart(deleteCHeartInput: DeleteCHeartInput, 
                        parent_id: str = Depends(JWTBearer()))-> CHeart:
    try:
        result = cheartService.deleteCHeart(deleteCHeartInput, parent_id)
    except CustomException as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete cheart")
    return result