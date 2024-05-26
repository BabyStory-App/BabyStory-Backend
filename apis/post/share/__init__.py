from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer

from services.share import ShareService
from schemas.share import *

router = APIRouter(
    prefix="/share",
    tags=["share"],
    responses={404: {"description": "Not found"}},
)

shareService = ShareService()

# 공유 생성
@router.post("/shareCreate", dependencies=[Depends(JWTBearer())])
async def create_share(createShareInput: CreateShareInput, 
                        parent_id: str = Depends(JWTBearer()))-> Share:
    """
    공유 생성
    --input
        - createShareInput.post_id: 게시물 아이디
        - parent_id: 공유한 부모 아이디
    --output
        - Share: 공유 딕셔너리
    """

    # 공유 생성
    result = shareService.createShare(createShareInput, parent_id)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="createshare not found")

    return result

# 공유 삭제
@router.delete("/shareDelete", dependencies=[Depends(JWTBearer())])
async def delete_share(deleteShareInput: DeleteShareInput, 
                        parent_id: str = Depends(JWTBearer()))-> Share:
    """
    공유 삭제
    --input
        - deleteShareInput.post_id: 게시물 아이디
        - parent_id: 공유한 부모 아이디
    --output
        - Share: 공유 딕셔너리
    """

    # 공유 삭제
    result = shareService.deleteShare(deleteShareInput, parent_id)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="deleteshare not found")

    return result