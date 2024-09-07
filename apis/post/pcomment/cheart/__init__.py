from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer
from services.cheart import CHeartService
from schemas.cheart import *
from error.exception.customerror import *

router = APIRouter(
    prefix="/cheart",
    tags=["cheart"],
    responses={404: {"description": "Not found"}},
)

cheartService = CHeartService()

# 하트 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_heart(createCHeartInput: CreateCHeartInput, 
                        parent_id: str = Depends(JWTBearer()))-> CHeart:
    try:
        result = cheartService.createCHeart(createCHeartInput, parent_id)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="create heart not found")
    return result

# 하트 삭제
@router.delete("/delete", dependencies=[Depends(JWTBearer())])
async def delete_heart(deleteCHeartInput: DeleteCHeartInput, 
                        parent_id: str = Depends(JWTBearer()))-> CHeart:
    try:
        result = cheartService.deleteCHeart(deleteCHeartInput, parent_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="delete heart not found")
    return result