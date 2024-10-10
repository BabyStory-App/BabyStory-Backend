from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer

from services.pview import PViewService
from schemas.pview import *
from error.exception.customerror import *

router = APIRouter(
    prefix="/pview",
    tags=["pview"],
    responses={404: {"description": "Not found"}},
)

pviewService = PViewService()

# view 관리
@router.post("/", dependencies=[Depends(JWTBearer())])
async def manage_view(managePViewInput: ManagePViewInput,
                        parent_id: str = Depends(JWTBearer()))-> ManagePViewOutput:
    try:
        result = pviewService.managePView(managePViewInput, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to manage pview")
    return {"hasCreated": result['hasCreated'], "message": result['message'], "pview": result['pview']}

# view 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_view(createPViewInput: CreatePViewInput, 
                        parent_id: str = Depends(JWTBearer()))-> CreatePViewOutput:
    try:
        result = pviewService.createPView(createPViewInput, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create pview")
    return {"success": 200, "message": "Success to create pview", "pview": result}

# view 삭제
@router.delete("/delete", dependencies=[Depends(JWTBearer())])
async def delete_view(deletePViewInput: DeletePViewInput, 
                        parent_id: str = Depends(JWTBearer()))-> DeletePViewOutput:
    try:
        result = pviewService.deletePView(deletePViewInput, parent_id)
    except CustomException as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete pview")
    return {"success": 200, "message": "Success to delete pview", "pview": result}