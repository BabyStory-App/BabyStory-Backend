from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer

from services.pheart import PHeartService
from schemas.pheart import *
from error.exception.customerror import *

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
    try:
        result = pheartService.createPHeart(createPHeartInput, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create pheart")
    return result

# 하트 삭제
@router.delete("/delete", dependencies=[Depends(JWTBearer())])
async def delete_heart(deletePHeartInput: DeletePHeartInput, 
                        parent_id: str = Depends(JWTBearer()))-> PHeart:
    try:
        result = pheartService.deletePHeart(deletePHeartInput, parent_id)
    except CustomException as e:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete pheart")
    return result