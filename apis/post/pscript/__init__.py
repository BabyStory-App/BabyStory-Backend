from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer

from services.pscript import PScriptService
from schemas.pscript import *

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
    """
    스크립트 생성
    --input
        - createScriptInput.post_id: 게시물 아이디
        - parent_id: 스크립트한 부모 아이디
    --output
        - PScript: 스크립트 딕셔너리
    """

    # 스크립트 생성
    result = pscriptService.createPScript(createPScriptInput, parent_id)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create pscript")
    
    return result

# 스크립트 삭제
@router.delete("/delete", dependencies=[Depends(JWTBearer())])
async def delete_pscript(deletePScriptInput: DeletePScriptInput, 
                        parent_id: str = Depends(JWTBearer()))-> PScript:
    """
    스크립트 삭제
    --input
        - deleteScriptInput.post_id: 게시물 아이디
        - parent_id: 스크립트한 부모 아이디
    --output
        - PScript: 스크립트 딕셔너리
    """

    # 스크립트 삭제
    result = pscriptService.deletePScript(deletePScriptInput, parent_id)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete pscript")
    
    return result