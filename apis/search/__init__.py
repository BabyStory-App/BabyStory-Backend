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
@router.post("/recommend/{type}", dependencies=[Depends(JWTBearer())])
async def create_recommend( createSearchRecommendInput: CreateSearchRecommendInput, parent_id: str = Depends(JWTBearer())):
    """
    추천 페이지 생성
    --input
        - createSearchRecommendInput.type: 짝꿍이야기, 친구이야기, 이웃이야기(friend, friend_read, neighbor)
        - createSearchRecommendInput.size: 게시물 개수
        - createSearchRecommendInput.page: 페이지 수
    --output
        - List<{postid, photoid, title, author_photo, author_name}> : 짝꿍이야기
        - List<{postid, photoid, title, heart, comment, author_name, desc}> : 친구이야기, 이웃이야기
    """
    # 부모 아이디가 없으면 에러
    if parent_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")

    # 타입이 없으면 에러
    if createSearchRecommendInput.type is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid type")

    # size가 없으면 에러
    if createSearchRecommendInput.size is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid size")

    # page가 없으면 에러
    if createSearchRecommendInput.page is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid page")

    # 짝꿍이 쓴 게시물
    if createSearchRecommendInput.type == 'friend':
        result = await postMainService.createPostMainFriend(parent_id, createSearchRecommendInput.size, createSearchRecommendInput.page)

        if result is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="createpostmainfriend not found")

    # 친구가 쓴 게시물
    elif createSearchRecommendInput.type == 'friend_read':
        result = await postMainService.createPostMainFriendRead(parent_id, createSearchRecommendInput.size, createSearchRecommendInput.page)

        if result is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="createpostmainfriendread not found")
                
    # 이웃들이 쓴 게시물
    elif createSearchRecommendInput.type == 'neighbor':
        result = await postMainService.createPostMainNeighbor(parent_id, createSearchRecommendInput.size, createSearchRecommendInput.page)

        if result is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="createpostmainneighbor not found")
        
    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Recommend not found")

    # 결과값 리턴
    return {    
        "result" : result
        }


# 검색결과 페이지 생성
@router.post("/result/{search}", dependencies=[Depends(JWTBearer())])
async def create_result(createSearchInput: CreateSearchInput, parent_id: str = Depends(JWTBearer())):
    """
    검색결과 페이지 생성
    --input
        - createSearchInput.search: 검색어
        - createSearchInput.size: 게시물 개수
        - createSearchInput.page: 페이지 수
    --output
        - search: 검색어
        - List<{title, photoid,  author_name, heart, commnet, desc}> : 검색결과
    """
    # 부모 아이디가 없으면 에러
    if parent_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")

    # 검색어가 없으면 에러
    if createSearchInput.search is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid search")

    # n이 없으면 에러
    if createSearchInput.size is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid size")

    # page가 없으면 에러
    if createSearchInput.page is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid page")

    # 검색 결과 생성
    result = await searchService.createSearch(createSearchInput.search, createSearchInput.size, createSearchInput.page)

    if result is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="createSearch not found")

    # 검색어와 결과값 리턴
    return {    
        "search" : createSearchInput.search,
        "result" : result
        }




# asnc, await schema
# 주석처리
# 테스트

# 기존 postmain에서 n과 페이지설정








