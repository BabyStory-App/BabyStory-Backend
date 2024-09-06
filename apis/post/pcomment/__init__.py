from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Header
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer

from services.pcomment import PCommentService
from schemas.pcomment import *
from error.exception.customerror import *

router = APIRouter(
    prefix="/pcomment",
    tags=["pcomment"],
    responses={404: {"description": "Not found"}},
)
pcommentService = PCommentService()

# 댓글 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_pcomment(createCommentInput: CreatePCommentInput,
                parent_id: str = Depends(JWTBearer()))-> CreatePCommentOutput:
    try:
        pcomment = pcommentService.createPComment(parent_id, createCommentInput)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create pcomment")
    return { 'pcomment': pcomment }

# 모든 댓글 가져오기
@router.get("/all", dependencies=[Depends(JWTBearer())])
async def get_all_comment(post_id: int) -> List[PComment]:
    try:
        comment = pcommentService.getAllPComment(post_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get all comment")
    return comment

# 댓글에 대댓글이 있는 경우 대댓글 가져오기
@router.get("/reply", dependencies=[Depends(JWTBearer())])
async def get_reply_comment(comment_id: int) -> List[PComment]:
    try:
        comment = pcommentService.getReplyPComment(comment_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get all reply comment")
    return comment

# 댓글 수정
@router.put("/update", dependencies=[Depends(JWTBearer())])
async def update_comment(updatePCommentInput: UpdatePCommentInput,
                parent_id: str = Depends(JWTBearer())) -> UpdatePCommentOutput:
    try:
        pcomment = await pcommentService.updatePComment(updatePCommentInput, parent_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to update comment")
    return { "success": 200 if pcomment else 403, 'pcomment': pcomment }

# 댓글 삭제
@router.put("/delete", dependencies=[Depends(JWTBearer())])
async def delete_comment(deleteCommentInput: DeletePCommentInput,
                parent_id: str = Depends(JWTBearer())) -> DeletePCommentOutput:
    try:
        pcomment = await pcommentService.deletePComment(deleteCommentInput, parent_id)
    except CustomException as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete comment")
    return { "success": 200 if pcomment else 403, 'pcomment': pcomment }