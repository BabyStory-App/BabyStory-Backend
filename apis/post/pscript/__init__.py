from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer

from services.pscript import PScriptService
from schemas.pscript import *
from error.exception.customerror import *

router = APIRouter(
    prefix="/pscript",
    tags=["pscript"],
    responses={404: {"description": "Not found"}},
)

pscriptService = PScriptService()

# 스크립트 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_pscript(createPScriptInput: CreatePScriptInput, 
                        parent_id: str = Depends(JWTBearer()))-> PScript:
    try:
        result = pscriptService.createPScript(createPScriptInput, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create pscript")
    
    return result

# 스크립트 삭제
@router.delete("/delete", dependencies=[Depends(JWTBearer())])
async def delete_pscript(deletePScriptInput: DeletePScriptInput, 
                        parent_id: str = Depends(JWTBearer()))-> PScript:
    try:
        result = pscriptService.deletePScript(deletePScriptInput, parent_id)
    except CustomException as e:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete pscript")
    
    return result