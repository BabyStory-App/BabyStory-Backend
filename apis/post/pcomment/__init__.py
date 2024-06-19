from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Header
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer

from services.pcomment import PCommentService

from schemas.pcomment import *

router = APIRouter(
    prefix="/pcomment",
    tags=["pcomment"],
    responses={404: {"description": "Not found"}},
)

pcommentService = PCommentService()

# 댓글 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_comment(createCommentInput: CreatePCommentInput,
                parent_id: str = Depends(JWTBearer()))-> CreatePCommentOutput:
    
    # 부모 아이디가 없으면 에러
    if parent_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")
    
    pcomment = pcommentService.createPComment(parent_id, createCommentInput)

    if pcomment is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Comment not found")
    
    return { 'pcomment': pcomment }



# 모든 댓글 가져오기
@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_all_comment(post_id: int) -> List[PComment]:

    # 게시물 아이디가 없으면 에러
    if post_id == None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid post_id")
    
    comment = pcommentService.getAllPComment(post_id)

    if comment is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Comment not found")
    
    return comment



# 댓글에 대댓글이 있는 경우 대댓글 가져오기
@router.get("/reply", dependencies=[Depends(JWTBearer())])
async def get_reply_comment(comment_id: int) -> List[PComment]:
    
        # 댓글 아이디가 없으면 에러
        if comment_id == None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Invalid comment_id")
        
        comment = pcommentService.getReplyPComment(comment_id)
    
        if comment is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Comment not found")
        
        return comment



# 댓글 수정
@router.put("/update", dependencies=[Depends(JWTBearer())])
async def update_comment(updateCommentInput: UpdatePCommentInput,
                parent_id: str = Depends(JWTBearer())) -> UpdatePCommentOutput:
    
    # 부모 아이디가 없으면 에러
    if parent_id == None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")
    
    comment = pcommentService.updatePComment(parent_id, updateCommentInput)

    if comment is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Comment not found")
    
    return { 'comment': comment }



# 댓글 삭제
@router.delete("/delete", dependencies=[Depends(JWTBearer())])
async def delete_comment(deleteCommentInput: DeletePCommentInput,
                parent_id: str = Depends(JWTBearer())) -> DeletePCommentOutput:
    
    # 부모 아이디가 없으면 에러
    if parent_id == None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")
    
    comment = pcommentService.deletePComment(parent_id, deleteCommentInput)

    if comment is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Comment not found")
    
    return { 'comment': comment }