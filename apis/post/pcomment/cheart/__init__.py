from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
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
                        parent_id: str = Depends(JWTBearer()))-> ManageCHeartOutput:
    try:
        result = cheartService.manageCHeart(manageCHeartInput, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to manage cheart")
    return {"hasCreated": result['hasCreated'], "message": result['message'], "cheart": result['cheart']}


# 댓글 하트 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_heart(createCHeartInput: CreateCHeartInput, 
                        parent_id: str = Depends(JWTBearer()))-> CreateCHeartOutput:
    try:
        result = cheartService.createCHeart(createCHeartInput, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create cheart")
    return {"success": 200, "message": "Success to create cheart", "cheart": result}


# 댓글 하트 삭제
@router.delete("/delete", dependencies=[Depends(JWTBearer())])
async def delete_heart(deleteCHeartInput: DeleteCHeartInput, 
                        parent_id: str = Depends(JWTBearer()))-> DeleteCHeartOutput:
    try:
        result = cheartService.deleteCHeart(deleteCHeartInput, parent_id)
    except CustomException as e:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete cheart")
    return {"success": 200, "message": "Success to delete cheart", "cheart": result}


# 댓글 하트 조회
@router.get("/hasHeart/{comment_id}", dependencies=[Depends(JWTBearer())])
async def has_heart(comment_id: str, parent_id: str = Depends(JWTBearer()))-> HasHeartOutput:
    try:
        result = cheartService.hasHeart(comment_id, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get cheart")
    return {"hasHeart": result}