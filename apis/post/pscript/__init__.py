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

# 스크립트 관리
@router.post("/", dependencies=[Depends(JWTBearer())])
async def manage_pscript(managePScriptInput: ManagePScriptInput,
                        parent_id: str = Depends(JWTBearer()))-> ManagePScriptOutput:
    try:
        result = pscriptService.managePScript(managePScriptInput, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to manage pscript")
    return {"hasCreated": result['hasCreated'], "message": result['message'], "pscript": result['pscript']}


# 스크립트 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_pscript(createPScriptInput: CreatePScriptInput, 
                        parent_id: str = Depends(JWTBearer()))-> CreatePScriptOutput:
    try:
        result = pscriptService.createPScript(createPScriptInput, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create pscript")
    return {"success": 200, "message": "Success to create pscript", "pscript": result}


# 스크립트 삭제
@router.delete("/delete", dependencies=[Depends(JWTBearer())])
async def delete_pscript(deletePScriptInput: DeletePScriptInput, 
                        parent_id: str = Depends(JWTBearer()))-> DeletePScriptOutput:
    try:
        script = pscriptService.deletePScript(deletePScriptInput, parent_id)
    except CustomException as e:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete pscript")
    return {"success": 200, "message": "Success to delete pscript", "pscript": script}


# 스크립트 조회
@router.get("/hasScript/{post_id}", dependencies=[Depends(JWTBearer())])
async def has_script(post_id: int,
                     parent_id: str = Depends(JWTBearer()))-> HasScriptOutput:
    try:
        script = pscriptService.hasScript(post_id, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to check script")
    return {"status": 200, "message": f"Successfully get Script of {post_id}", "state": script}