from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from typing import Union, Optional
import bcrypt

from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer

from services.parent import ParentService

from schemas.parent import *
from error.exception.customerror import *


router = APIRouter(
    prefix="/parent",
    tags=["parent"],
    responses={404: {"description": "Not found"}},
)
parentService = ParentService()

# 부모 생성
@router.post("/")
def create_parent(createParentInput: CreateParentInput) -> CreateParentOutput:
    try:
        parent = parentService.createParent(createParentInput)

        if parent is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Parent not found")

    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create parent")

    parent_data = {
        'parent_id': parent.parent_id,
        'password': parent.password,
        'email': parent.email,
        'name': parent.name,
        'nickname': parent.nickname,
        'gender': parent.gender,
        'signInMethod': parent.signInMethod,
        'emailVerified': parent.emailVerified,
        'photoId': parent.photoId,
        'description': parent.description,
        'mainAddr': parent.mainAddr,
        'subAddr': parent.subAddr,
        'hashList': parent.hashList
    }

    return JSONResponse(status_code=201, content={
        'parent': parent_data,
        'x-jwt': signJWT(parent.parent_id)
    })


# 부모 정보 조회
@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_parent(parent_id: str = Depends(JWTBearer())) -> GetParentByEmailOutput:
    parent = parentService.getParent(parent_id)

    if parent is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Parent not found")

    parent_data = {
        'parent_id': parent.parent_id,
        'password': parent.password,
        'email': parent.email,
        'name': parent.name,
        'nickname': parent.nickname,
        'gender': parent.gender,
        'signInMethod': parent.signInMethod,
        'emailVerified': parent.emailVerified,
        'photoId': parent.photoId,
        'description': parent.description,
        'mainAddr': parent.mainAddr,
        'subAddr': parent.subAddr,
        'hashList': parent.hashList
    }

    return JSONResponse(status_code=200, content={
        'parent': parent_data,
        'x-jwt': signJWT(parent.parent_id)
    })


# 부모 정보 수정
@router.put("/", dependencies=[Depends(JWTBearer())])
async def update_parent(updateParentInput: UpdateParentInput,
                        parent_id: str = Depends(JWTBearer())) -> UpdateParentOutput:
    if updateParentInput.gender != None and updateParentInput.gender not in [0, 1, 2]:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Gender must be 0, 1, 2"
        )

    parent = parentService.updateParent(parent_id, updateParentInput)

    if parent is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Update failed")
    return {
        "success": 200 if parent else 403,
        "parent": parent
    }


# 프로필 이미지 업로드
@router.post("/upload/profile", dependencies=[Depends(JWTBearer())])
async def upload_profile_image(file: Optional[UploadFile] = None, parent_id: str = Depends(JWTBearer())) -> UploadProfileImageOutput:
    try:
        success = parentService.uploadProfileImage(file, parent_id)

        if success == False:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Parent not found")

    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Upload failed")

    return {
        "success": 200 if success else 403,
        "photoId": parent_id
    }


# 부모 삭제
@router.delete("/", dependencies=[Depends(JWTBearer())])
async def delete_parent(parent_id: str = Depends(JWTBearer())) -> DeleteParentOutput:
    if parent_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Parent not found")

    parent = parentService.deleteParent(parent_id)

    return {
        "success": 200 if parent else 403,
    }


# 이메일로 부모 목록 조회
@router.get("/friends")
async def get_friends(emails: str = Header(None)):
    email_list = emails.split(',') if emails is not None else []
    print(email_list)
    try:
        friends_dict = parentService.getFriends(email_list)

    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get friends")

    return {
        "friends": friends_dict
    }


# 부모에게 다른 아기 pbconnect 요청
@router.post("/pbconnect")
async def create_pbconnect(baby_id: str, parent_id: str = Depends(JWTBearer())) -> CreatePBConnectOutput:
    pbconnect = parentService.create_pbconnect(baby_id, parent_id)

    if pbconnect is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="PBConnect not found")

    return {
        "success": 200 if pbconnect else 403,
    }


@router.get("/all")
async def get_parent():
    '''
    임시코드
    '''
    parent = parentService.getParentAll()

    return parent


# 부모 로그인
@router.post("/login")
async def login_parent(createLoginInput: CreateLoginInput) -> CreateLoginOutput:
    try:
        parent = parentService.createLogin(createLoginInput)
        parent_data = {
            'parent_id': parent.parent_id,
            'password': parent.password,
            'email': parent.email,
            'name': parent.name,
            'nickname': parent.nickname,
            'gender': parent.gender,
            'signInMethod': parent.signInMethod,
            'emailVerified': parent.emailVerified,
            'photoId': parent.photoId,
            'description': parent.description,
            'mainAddr': parent.mainAddr,
            'subAddr': parent.subAddr,
            'hashList': parent.hashList
        }

    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)

    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to login")

    return JSONResponse(status_code=200, content={
        'parent': parent_data,
        'x-jwt': signJWT(parent.parent_id)
    })
