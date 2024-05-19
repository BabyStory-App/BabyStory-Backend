from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer

from services.script import ScriptService
from schemas.script import *

router = APIRouter(
    prefix="/script",
    tags=["script"],
    responses={404: {"description": "Not found"}},
)

scriptService = ScriptService()

# 스크립트 생성
@router.post("/scriptCreate", dependencies=[Depends(JWTBearer())])
async def create_script(createScriptInput: CreateScriptInput, 
                        parent_id: str = Depends(JWTBearer()))-> Script:
    """
    스크립트 생성
    --input
        - createScriptInput.post_id: 게시물 아이디
        - parent_id: 스크립트한 부모 아이디
    --output
        - Script: 스크립트 딕셔너리
    """

    # 스크립트 생성
    result = scriptService.createScript(createScriptInput, parent_id)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="createscript not found")
    
    return result

# 스크립트 삭제
@router.delete("/scriptDelete", dependencies=[Depends(JWTBearer())])
async def delete_script(deleteScriptInput: DeleteScriptInput, 
                        parent_id: str = Depends(JWTBearer()))-> Script:
    """
    스크립트 삭제
    --input
        - deleteScriptInput.post_id: 게시물 아이디
        - parent_id: 스크립트한 부모 아이디
    --output
        - Script: 스크립트 딕셔너리
    """

    # 스크립트 삭제
    result = scriptService.deleteScript(deleteScriptInput, parent_id)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="deletescript not found")
    
    return result