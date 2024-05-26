from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer

from services.view import ViewService
from schemas.view import *

router = APIRouter(
    prefix="/view",
    tags=["view"],
    responses={404: {"description": "Not found"}},
)

viewService = ViewService()

# 조회 생성
@router.post("/viewCreate", dependencies=[Depends(JWTBearer())])
async def create_view(createViewInput: CreateViewInput, 
                        parent_id: str = Depends(JWTBearer()))-> View:
    """
    조회 생성
    --input
        - createViewInput.post_id: 게시물 아이디
        - parent_id: 조회한 부모 아이디
    --output
        - View: 조회 딕셔너리
    """

    # 조회 생성
    result = viewService.createView(createViewInput, parent_id)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="createview not found")
    
    return result

# 조회 삭제
@router.delete("/viewDelete", dependencies=[Depends(JWTBearer())])
async def delete_view(deleteViewInput: DeleteViewInput, 
                        parent_id: str = Depends(JWTBearer()))-> View:
    """
    조회 삭제
    --input
        - deleteViewInput.post_id: 게시물 아이디
        - parent_id: 조회한 부모 아이디
    --output
        - View: 조회 딕셔너리
    """

    # 조회 삭제
    result = viewService.deleteView(deleteViewInput, parent_id)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="deleteview not found")
    
    return result