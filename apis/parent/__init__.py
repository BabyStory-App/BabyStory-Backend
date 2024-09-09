from fastapi import APIRouter, HTTPException, Depends, Header
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
    '''
    부모 생성
    --input
        - createParentInput.parent_id: 부모 아이디
        - createParentInput.email: 이메일
        - createParentInput.password: 비밀번호
        - createParentInput.nickname: 닉네임
        - createParentInput.signInMethod: 로그인 방식
        - createParentInput.emailVerified: 이메일 인증 여부
    --output
        - parent: 부모 정보
        - x-jwt: JWT 토큰
    '''
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
    '''
    부모 정보 조회
    --input
        - parent_id: 부모 아이디
    --output
        - parent: 부모 정보
        - x-jwt: JWT 토큰
    '''

    if parent_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")

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
    '''
    부모 정보 수정
    --input\
        - updateParentInput.password: 비밀번호
        - updateParentInput.email: 이메일
        - updateParentInput.name: 이름
        - updateParentInput.nickname: 닉네임
        - updateParentInput.gender: 성별 (0: 남성, 1: 여성, 2: 기타)
        - updateParentInput.signInMethod: 로그인 방식
        - updateParentInput.emailVerified: 이메일 인증 여부
        - updateParentInput.photoId: 사진 아이디
        - updateParentInput.description: 설명
        - updateParentInput.mainAddr: 주소
        - updateParentInput.subAddr: 상세 주소
        - updateParentInput.hashList: 해시 리스트
    --output
        - success: 성공 여부
        - parent: 부모 정보
    '''
    if updateParentInput.gender not in [0, 1, 2]:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Gender must be 0, 1, 2"
        )

    if parent_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Parent not found")

    parent = parentService.updateParent(parent_id, updateParentInput)

    if parent is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Update failed")

    return {
        "success": 200 if parent else 403,
        "parent": parent
    }

# 부모 삭제


@router.delete("/", dependencies=[Depends(JWTBearer())])
async def delete_parent(parent_id: str = Depends(JWTBearer())) -> DeleteParentOutput:
    '''
    부모 삭제
    --input
        - parent_id: 부모 아이디
    --output
        - success: 성공 여부
    '''
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
    '''
    이메일로 부모의 대략적인 정보 조회
    --input
        - emails: 이메일
    --output
        - friends: 부모 정보
    '''
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
    '''
    부모에게 다른 아기 연결 요청 (부부끼리 아기를 공유할 수 있음)
    --input
        - baby_id: 아기 아이디
        - parent_id: 부모 아이디
    --output
        - success: 성공 여부
    '''
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


@router.post("/login")
async def login_parent(createLoginInput: CreateLoginInput) -> CreateLoginOutput:
    '''
    부모 로그인
    --input
        - createLoginInput.email: 이메일
        - createLoginInput.password: 비밀번호
    --output
        - parent: 부모 정보
        - x-jwt: JWT 토큰
    '''
    try:
        parent = parentService.createLogin(createLoginInput)

    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)

    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to login")

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
