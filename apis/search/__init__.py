from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer

from services.search import SearchService
from services.postmain import PostMainService
from schemas.search import *
from schemas.postmain import *


router = APIRouter(
    prefix="/post/search",
    tags=["/post/search"],
    responses={404: {"description": "Not found"}},
)

searchService = SearchService()
postMainService = PostMainService()

# 추천 페이지 생성
@router.post("/recommand/{type}", dependencies=[Depends(JWTBearer())])
async def create_recommand(type: str, size: int, page: int, parent_id: str = Depends(JWTBearer())):
    """
    추천 페이지 생성
    --input
        - type: 짝꿍이야기, 친구이야기, 이웃이야기(friend, friend_read, neighbor)
        - size: 게시물 개수
        - page: 페이지 수
    --output
        - List<{postid, photoid, title, author_photo, author_name}> : 짝꿍이야기
        - List<{postid, photoid, title, heart, comment, author_name, desc}> : 친구이야기, 이웃이야기
    """
    # 부모 아이디가 없으면 에러
    if parent_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")

    # 타입이 없으면 에러
    if type is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid type")

    # size가 없으면 에러
    if size is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid size")

    # page가 없으면 에러
    if page is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid page")

    # 짝꿍이 쓴 게시물
    if type == 'friend':
        result = await postMainService.createPostMainFriend(parent_id, size, page)

        if result is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="createpostmainfriend not found")

    # 친구가 쓴 게시물
    elif type == 'friend_read':
        result = await postMainService.createPostMainFriendRead(parent_id, size, page)

        if result is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="createpostmainfriendread not found")
                
    # 이웃들이 쓴 게시물
    elif type == 'neighbor':
        result = await postMainService.createPostMainNeighbor(parent_id, size, page)

        if result is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="createpostmainneighbor not found")

    # 결과값 리턴
    return {    
        "result" : result
        }


# 검색결과 페이지 생성
@router.post("/result/{search}", dependencies=[Depends(JWTBearer())])
async def create_result(search: str, n: int, page: int, parent_id: str = Depends(JWTBearer())):
    # 부모 아이디가 없으면 에러
    if parent_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")

    # 검색어가 없으면 에러
    if search is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid search")

    # n이 없으면 에러
    if n is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid n")

    # page가 없으면 에러
    if page is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid page")

    # 검색 결과 생성
    result = await searchService.createSearch(search, n, page)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="createSearch not found")

    # 검색어와 결과값 리턴
    return {    
        "search" : search,
        "result" : result
        }

# asnc, await
# 주석처리
# 테스트


# 기존 postmain에서 n과 페이지설정








