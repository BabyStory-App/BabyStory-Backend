from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Header
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
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
async def create_post(createPostInput: CreatePostInput,
                      parent_id: str = Depends(JWTBearer())) -> CreatePostOutput:

    try:
        post = postService.createPost(parent_id, createPostInput)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create post")
    
    return {'post': post}



# 새로 생성된 post 사진 업로드
@router.post("/photoUpload", dependencies=[Depends(JWTBearer())])
async def upload_photo(fileList: List[UploadFile],
                       post_id: int = Header(default=None),
                       parent_id: str = Depends(JWTBearer())) -> UploadPhotoOutput:
    
    success = postService.uploadPhoto(fileList, post_id, parent_id)

    return { 'success': success }
    


# 모든 게시물 가져오기
@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_all_post(parent_id: str = Depends(JWTBearer())) -> List[Post]:

    # 부모 아이디가 없으면 에러
    if parent_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")
    
    # 게시물 정보 가져오기
    post = await postService.getAllPost(parent_id)

    if post is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="post not found")
    
    return post



# 하나의 게시물 가져오기
@router.get("/{post_id}", dependencies=[Depends(JWTBearer())])
async def get_post(post_id: str, parent_id: str = Depends(JWTBearer())) -> Optional[Post]:

    # 부모 아이디가 없으면 에러
    if parent_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")
    
    # 게시물 정보 가져오기
    post = await postService.getPost(post_id, parent_id)

    if post is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="post not found")
    
    return post



# 게시물 수정
@router.put("/{post_id}", dependencies=[Depends(JWTBearer())])
async def update_post(updatePostInput: UpdatePostInput,
                parent_id:str = Depends(JWTBearer())) -> UpdatePostOutput:
    
    # 부모 아이디가 없으면 에러
    if parent_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")
    
    # 게시물 정보 수정
    post = await postService.updatePost(updatePostInput, parent_id)

    if post is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="post not found")
    
    return{ "success": 200 if post else 403, "post": post }



# 게시물 삭제
@router.put("/delete/{post_id}", dependencies=[Depends(JWTBearer())])
async def delete_post(deletePostInput: DeletePostInput,
                parent_id:str = Depends(JWTBearer()))-> DeletePostOutput:
    
    # 부모 아이디가 없으면 에러
    if parent_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")
    
    # 게시물 삭제
    success = await postService.deletePost(deletePostInput, parent_id)
   
    if success is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="post not found")
    
    return{ "success": 200 if success else 403, "post": success}