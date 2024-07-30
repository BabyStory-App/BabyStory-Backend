from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Header, Form
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
async def get_overview(parent_id: str = Depends(JWTBearer())) -> SettingOverviewOutput:
    try:
        overview = settingService.getOverview(parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get overview")
    return {'status': 'success', 'message': 'Successfully get overview', 'data': overview}



# 친구들 불러오기
@router.get("/myfriends/{page}", dependencies=[Depends(JWTBearer())])
async def get_my_friends(page: int, parent_id: str = Depends(JWTBearer())) -> MyFriendsOutput:
    try:
        myFriends = settingService.getMyFriends(page, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get my friends")
    return {'status': 'success', 'message': 'Successfully get my friends', 'paginationInfo': myFriends['paginationInfo'], 'parents': myFriends['parents']}



# 유저가 조회한 post
@router.get("/myviews/{page}", dependencies=[Depends(JWTBearer())])
async def get_my_views(page: int, parent_id: str = Depends(JWTBearer())) -> MyViewsPostOutput:
    try:
        myViews = settingService.getMyViews(page, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get my views")
    return {'status': 'success', 'message': 'Successfully get my views', 'paginationInfo': myViews['paginationInfo'], 'post': myViews['post']}



# 유저가 script한 post
@router.get("/scripts/{page}", dependencies=[Depends(JWTBearer())])
async def get_scripts(page: int, parent_id: str = Depends(JWTBearer())) -> MyViewsPostOutput:
    try:
        scripts = settingService.getScripts(page, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get scripts")
    return {'status': 'success', 'message': 'Successfully get scripts', 'paginationInfo': scripts['paginationInfo'], 'post': scripts['post']}



# 유저가 좋아요한 post
@router.get("/likes/{page}", dependencies=[Depends(JWTBearer())])
async def get_likes(page: int, parent_id: str = Depends(JWTBearer())) -> MyViewsPostOutput:
    try:
        likes = settingService.getLikes(page, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get likes")
    return {'status': 'success', 'message': 'Successfully get likes', 'paginationInfo': likes['paginationInfo'], 'post': likes['post']}



# 유저 post
@router.get("/mystories/{page}", dependencies=[Depends(JWTBearer())])
async def get_my_stories(page: int, parent_id: str = Depends(JWTBearer())) -> MyStoriesOutput:
    try:
        myStories = settingService.getMyStories(page, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get my stories")
    return {'status': 'success', 'message': 'Successfully get my stories', 'paginationInfo': myStories['paginationInfo'], 'post': myStories['post']}



# 유저의 짝꿍 불러오기
@router.get("/mymates/{page}", dependencies=[Depends(JWTBearer())])
async def get_my_mates(page: int, parent_id: str = Depends(JWTBearer())) -> MyMatesOutput:
    try:
        myMates = settingService.getMyMates(page, parent_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get my mates")
    return {'status': 'success', 'message': 'Successfully get my mates', 'paginationInfo': myMates['paginationInfo'], 'parents': myMates['parents']}