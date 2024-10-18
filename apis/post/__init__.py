from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Header, Form
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer

import os
from constants.path import *
from db import get_db_session
from services.setting import SettingService
from services.postmain import PostMainService
from services.post import PostService
from schemas.post import *
from error.exception.customerror import *


router = APIRouter(
    prefix="/post",
    tags=["post"],
    responses={404: {"description": "Not found"}},
)

db = get_db_session()

postService = PostService()
settingService = SettingService()
postMainService = PostMainService()


# 게시물 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_post(createPostInput: CreatePostInput,
                      parent_id: str = Depends(JWTBearer())) -> CreatePostOutput:
    try:
        post = postService.createPost(parent_id, createPostInput)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create post")
    return {'post': post}


# 새로 생성된 post 사진 업로드
@router.post("/photoUpload/{post_id}", dependencies=[Depends(JWTBearer())])
async def upload_post_photo(fileList: List[UploadFile],
                            post_id: int,
                            parent_id: str = Depends(JWTBearer())) -> UploadPhotoOutput:
    try:
        success = postService.uploadPhoto(fileList, post_id, parent_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to upload photo")
    return {'success': success}


# 모든 게시물 가져오기
@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_all_post(parent_id: str = Depends(JWTBearer())) -> List[Post]:
    try:
        post = await postService.getAllPost()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get all post")
    return post


# 특정 부모의 모든 게시물 가져오기
@router.get("/parent/{parent_id}/{limit}", dependencies=[Depends(JWTBearer())])
async def get_all_post_by_parent(parent_id: str, limit: Optional[int], uid: str = Depends(JWTBearer())):
    try:
        post = await postService.getAllPostByParent(parent_id, limit)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get all post")
    return post


# 하나의 게시물 가져오기
@router.get("/{post_id}", dependencies=[Depends(JWTBearer())])
async def get_post(post_id: str, parent_id: str = Depends(JWTBearer())):
    try:
        post = await postService.getPost(post_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get post")
    return post


# 게시물 수정
@router.put("/update/{post_id}", dependencies=[Depends(JWTBearer())])
async def update_post(updatePostInput: UpdatePostInput,
                      parent_id: str = Depends(JWTBearer())) -> UpdatePostOutput:
    try:
        post = await postService.updatePost(updatePostInput, parent_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to update post")
    return {"success": 200 if post else 403, "post": post}


# 게시물 post 사진 수정
@router.put("/photoUpdate/{post_id}", dependencies=[Depends(JWTBearer())])
async def update_post_photo(fileList: List[UploadFile],
                            post_id: int,
                            parent_id: str = Depends(JWTBearer())) -> UpdatePhotoOutput:
    try:
        success = await postService.updatePhoto(fileList, post_id, parent_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to update photo")
    return {'success': success, 'message': 'Success to update photo'}


# 게시물 삭제
@router.delete("/delete/{post_id}", dependencies=[Depends(JWTBearer())])
async def delete_post(deletePostInput: DeletePostInput,
                      parent_id: str = Depends(JWTBearer())) -> DeletePostOutput:
    try:
        success = await postService.deletePost(deletePostInput, parent_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete post")
    return {"success": 200 if success else 403, "post": success}


# 해당 부모의 프로필과 모든 게시물 가져오기
@router.get("/poster/profile/{parent_id}", dependencies=[Depends(JWTBearer())])
async def get_poster_profile(parent_id: str) -> GetPosterProfileOutput:
    try:
        # parent_id가 없을 경우 에러
        if parent_id is None:
            raise CustomException("parent_id is required")

        # 존재하지 않는 부모일 경우 에러
        parent = db.query(ParentTable).filter(
            ParentTable.parent_id == parent_id).first()
        if parent is None:
            raise CustomException("Parent not found")

        counts = settingService.getOverview(parent_id)
        posts = db.query(PostTable).filter(
            PostTable.parent_id == parent_id).all()

    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get poster profile")

    return {'parent': {
        "parentId": parent_id,
        "photoId": parent_id + ".jpeg",
        "parentName": parent.nickname,
        "parentDesc": parent.description,
        "mateCount": counts['mateCount'],
        "friendCount": counts['friendCount'],
        "myStoryCount": counts['myStoryCount']},
        'posts': ({"postid": post.post_id,
                   **dict(zip(["photoId", "desc"], postMainService._get_photoId_and_desc(
                       open(os.path.join(POST_CONTENT_DIR,
                            f"{post.post_id}.txt"), 'r', encoding='UTF-8').read()
                   ))),
                   "title": post.title,
                   "pHeart": post.pHeart,
                   "comment": post.pComment,
                   "author_name": parent.name
                   } for post in posts)
    }
