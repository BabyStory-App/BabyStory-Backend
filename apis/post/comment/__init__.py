from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer

from services.comment import CommentService
from schemas.comment import *

router = APIRouter(
    prefix="/comment",
    tags=["comment"],
    responses={404: {"description": "Not found"}},
)

commentService = CommentService()

# 댓글 생성
@router.post("/commentCreate", dependencies=[Depends(JWTBearer())])
async def create_comment(createCommentInput: CreateCommentInput, 
                         parent_id: str = Depends(JWTBearer()))-> PComment:
    """
    댓글 생성
    --input
        - createCommentInput.comment_id: 댓글 아이디
        - createCommentInput.post_id: 게시물 아이디
        - createCommentInput.reply_id: 상위 댓글 아이디
        - createCommentInput.comment: 댓글 내용
        - createCommentInput.time: 댓글 생성 시간
        - createCommentInput.cheart: 댓글 하트 수
        - parent_id: 부모 댓글 아이디
    --output
        - Comment: 댓글
    """

    # 댓글 생성
    result = commentService.createComment(createCommentInput, parent_id)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="createcomment not found")

    return result

# 댓글 수정
@router.put("/commentUpdate", dependencies=[Depends(JWTBearer())])
async def update_comment(updateCommentInput: UpdateCommentInput,
                          parent_id: str = Depends(JWTBearer()))-> UpdateCommentOutput:
    """
    댓글 수정
    --input
        - updateCommentInput.comment_id: 댓글 아이디
        - updateCommentInput.comment: 댓글 내용
        - updateCommentInput.time: 댓글 수정 시간 datetime.now()
    --output
        - Comment: 댓글
    """

    # 댓글 수정
    success = commentService.updateComment(parent_id, updateCommentInput)

    if success is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="updatecomment not found")

    return{ "success": 200 if success else 403,
            "comment": success}

# 댓글 삭제
@router.delete("/commentDelete", dependencies=[Depends(JWTBearer())])
async def delete_comment(deleteCommentInput: DeleteCommentInput, 
                         parent_id: str = Depends(JWTBearer()))-> DeleteCommentOutput:
    """
    댓글 삭제
    --input
        - deleteCommentInput.comment_id: 댓글 아이디
        - deleteCommentInput.time: 댓글 삭제 시간 datetime.now()
    --output
        - Comment: 댓글
    """

    # 댓글 삭제
    success = commentService.deleteComment(parent_id, deleteCommentInput)

    if success is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="deletecomment not found")

    return{ "success": 200 if success else 403,
            "comment": success}

# 해당 게시물의 모든 댓글 가져오기
@router.get("/commentAll/{post_id}", dependencies=[Depends(JWTBearer())])
async def get_comment(post_id: str)-> List[PComment]:
    """
    해당 게시물의 모든 댓글 가져오기
    --input
        - post_id: 게시물 아이디
    --output
        - List<Comment>: 댓글 리스트
    """

    # 해당 게시물의 모든 댓글 가져오기
    result = commentService.getAllComment(post_id)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="getcomment not found")

    return result

