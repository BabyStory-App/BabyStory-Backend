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

# 하트 관리
@router.post("/", dependencies=[Depends(JWTBearer())])
async def manage_heart(managePHeartInput: ManagePHeartInput,
                        parent_id: str = Depends(JWTBearer()))-> ManagePHeartOutput:
    try:
        result = pheartService.managePHeart(managePHeartInput, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to manage pheart")
    return {"hasCreated": result['hasCreated'], "message": result['message'], "pheart": result['pheart']}

# 하트 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_heart(createPHeartInput: CreatePHeartInput, 
                        parent_id: str = Depends(JWTBearer()))-> CreatePHeartOutput:
    try:
        pheart = pheartService.createPHeart(createPHeartInput, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create pheart")
    return {"success": 200, "message": "Success to create pheart", "pheart": pheart}

# 하트 삭제
@router.delete("/delete", dependencies=[Depends(JWTBearer())])
async def delete_heart(deletePHeartInput: DeletePHeartInput, 
                        parent_id: str = Depends(JWTBearer()))-> DeletePHeartOutput:
    try:
        pheart = pheartService.deletePHeart(deletePHeartInput, parent_id)
    except CustomException as e:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete pheart")
    return {"success": 200, "message": "Success to delete pheart", "pheart": pheart}