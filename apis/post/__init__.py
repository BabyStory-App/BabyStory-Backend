from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer

from services.post import PostService

from schemas.post import *



router = APIRouter(
    prefix="/post",
    tags=["post"],
    responses={404: {"description": "Not found"}},
)

postService = PostService()

# 게시물 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
def create_post(createPostInput: CreatePostInput,
                parent_id: str = Depends(JWTBearer()))-> CreatePostOutput:
    
    post = postService.createPost(createPostInput)

    if post is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Post not found")
    
    return { 'post': post }

# 모든 게시물 가져오기
@router.get("/", dependencies=[Depends(JWTBearer())])
def get_post(parent_id: str = Depends(JWTBearer())) -> List[Post]:

    # 부모 아이디가 없으면 에러
    if parent_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")
    
    # 게시물 정보 가져오기
    post = postService.getAllPost(parent_id)

    if post is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="post not found")
    
    return post

# 하나의 게시물 가져오기
@router.get("/{post_id}", dependencies=[Depends(JWTBearer())])
def get_post(post_id: str, parent_id: str = Depends(JWTBearer())) -> Post:

    # 부모 아이디가 없으면 에러
    if parent_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")
    
    # 게시물 정보 가져오기
    post = postService.getPost(post_id)

    if post is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="post not found")
    
    return post

# 게시물 수정
@router.put("/", dependencies=[Depends(JWTBearer())])
def update_post(updatePostInput: UpdatePostInput,
                parent_id:str = Depends(JWTBearer())) -> UpdatePostOutput:
    
    # 부모 아이디가 없으면 에러
    if parent_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")
    
    # 게시물 정보 수정
    post = postService.updatePost(updatePostInput,parent_id)

    if post is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="post not found")
    
    return{ "success": 200 if post else 403, "post": post }

# 게시물 삭제
@router.put("/delete", dependencies=[Depends(JWTBearer())])
def delete_post(deletePostInput: DeletePostInput,
                parent_id:str = Depends(JWTBearer())) -> DeletePostOutput:
    
    # 부모 아이디가 없으면 에러
    if parent_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")
    
    # 게시물 삭제
    success = postService.deletePost(deletePostInput, parent_id)

    if success is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="post not found")
    
    return{ "success": 200 if success else 403 }