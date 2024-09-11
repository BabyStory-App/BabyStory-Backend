from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer

from services.setting import SettingService
from schemas.setting import *
from error.exception.customerror import *

router = APIRouter(
    prefix="/setting",
    tags=["setting"],
    responses={404: {"description": "Not found"}},
)

settingService = SettingService()



# 짝꿍, 친구들, 이야기 수 가져오기
@router.get("/overview", dependencies=[Depends(JWTBearer())])
async def get_overview(parent_id: str = Depends(JWTBearer())) -> SettingOverviewOutputService:
    try:
        overview = settingService.getOverview(parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get overview")
    return {'status': 200, 'message': 'Successfully get overview', 'data': overview}



# 친구들 불러오기
@router.get("/myfriends/{page}", dependencies=[Depends(JWTBearer())])
async def get_my_friends(page: int, parent_id: str = Depends(JWTBearer())) -> MyFriendsOutput:
    try:
        result = settingService.getMyFriends(page, parent_id)
        if(result == None):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Failed to get my friends")
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get my friends")
    return {'status': 'success', 'message': 'Successfully get my friends', 'paginationInfo': result['paginationInfo'], 'parents': result['parents']}



# 유저가 조회한 post
@router.get("/myviews/{page}", dependencies=[Depends(JWTBearer())])
async def get_my_views(page: int, parent_id: str = Depends(JWTBearer())) -> MyViewsPostOutput:
    try:
        print("------------------a1")
        result = settingService.getMyViews(page, parent_id)
        print("result: ", result)
        if(result == None):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Failed to get view post")
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get my view post")
    return {'status': 'success', 'message': 'Successfully get my views', 'paginationInfo': result['paginationInfo'], 'post': result['post']}



# 유저가 script한 post
@router.get("/scripts/{page}", dependencies=[Depends(JWTBearer())])
async def get_scripts(page: int, parent_id: str = Depends(JWTBearer())) -> MyScriptsPostOutput:
    try:
        result = settingService.getScripts(page, parent_id)
        if(result == None):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Failed to get script post")
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get script post")
    return {'status': 'success', 'message': 'Successfully get scripts', 'paginationInfo': result['paginationInfo'], 'post': result['post']}



# 유저가 좋아요한 post
@router.get("/likes/{page}", dependencies=[Depends(JWTBearer())])
async def get_likes(page: int, parent_id: str = Depends(JWTBearer())) -> MyLikesPostOutput:
    try:
        result = settingService.getLikes(page, parent_id)
        if(result == None):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Failed to get like post")
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get like post")
    return {'status': 'success', 'message': 'Successfully get likes', 'paginationInfo': result['paginationInfo'], 'post': result['post']}


# 유저 post
@router.get("/mystories/{page}", dependencies=[Depends(JWTBearer())])
async def get_my_stories(page: int, parent_id: str = Depends(JWTBearer())) -> MyStoriesOutput:
    try:
        print("a-------------------------")
        result = settingService.getMyStories(page, parent_id)
        if(result == None):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Failed to get my post")
        print("result : ", result)
        print("post", result['post'])
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get my post")
    return {'status': 'success', 'message': 'Successfully get my stories', 'paginationInfo': result['paginationInfo'], 'post': result['post']}


# 유저의 짝꿍 불러오기
@router.get("/mymates/{page}", dependencies=[Depends(JWTBearer())])
async def get_my_mates(page: int, parent_id: str = Depends(JWTBearer())) -> MyMatesOutput:
    try:
        result = settingService.getMyMates(page, parent_id)
        if(result == None):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Failed to get my mates")
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get my mates")
    return {'status': 'success', 'message': 'Successfully get my mates', 'paginationInfo': result['paginationInfo'], 'parents': result['parents']}