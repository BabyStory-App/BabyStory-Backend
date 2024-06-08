from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer

from services.postmain import PostMainService
from schemas.postmain import *


router = APIRouter(
    prefix="/main",
    tags=["main"],
    responses={404: {"description": "Not found"}},
)

postMainService = PostMainService()

# 메인페이지 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_postmain(parent_id: str = Depends(JWTBearer())):
    """
    메인페이지 생성
    --input
        - parent_id: 부모 아이디
    --output
        - banner: 메인페이지 배너
        - friend: 짝꿍이 쓴 게시물
        - friend_read: 친구가 쓴 게시물
        - neighbor: 친구로 등록되지 않은 이웃목록
        - neighbor_post: 이웃들이 쓴 게시물
        - highview: 조회수가 높은 게시물
        - hashtag: 많이 본 해시태그로 게시물 추천
    """
    # 부모 아이디가 없으면 에러
    if parent_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")

    # 메인페이지 배너
    createpostmain = postMainService.createPostMainBanner()

    if createpostmain is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="createpostmain not found")
    
    # 짝꿍이 쓴 게시물
    createpostmainfriend = postMainService.createPostMainFriend(CreatePostMainInput(parent_id=parent_id))

    if createpostmainfriend is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="createpostmainfriend not found")

    # 친구가 쓴 게시물
    createpostmainfriendread = postMainService.createPostMainFriendRead(CreatePostMainInput(parent_id=parent_id))

    if createpostmainfriendread is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="createpostmainfriendread not found")

    # 친구로 등록되지 않은 이웃목록

    getneighbor = postMainService.getNeighbor(parent_id)

    if getneighbor is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="neighbor not found")

    # 이웃들이 쓴 게시물
    createpostmainneighbor = postMainService.createPostMainNeighbor(CreatePostMainInput(parent_id=parent_id))

    if createpostmainneighbor is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="createpostmainneighbor not found")

    # 조회수가 높은 게시물
    createpostmainhighview = postMainService.createPostMainHighView()

    if createpostmainhighview is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="createpostmainhighview not found")

    # 많이 본 해시태그로 게시물 추천
    createpostmainhashtag = postMainService.createPostMainHashtag(parent_id)

    if createpostmainhashtag is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="createpostmainhashtag not found")


    return { 'banner' : createpostmain,
             'friend' : createpostmainfriend,
            'friend_read' : createpostmainfriendread,
            'neighbor' : getneighbor,
            'neighbor_post' : createpostmainneighbor,
            'highview' : createpostmainhighview,
            'hashtag' : createpostmainhashtag
             }










