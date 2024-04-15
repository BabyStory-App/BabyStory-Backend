from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from typing import Union, Optional

from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer

from services.parent import ParentService

from schemas.parent import *


router = APIRouter(
    prefix="/parent",
    tags=["parent"],
    responses={404: {"description": "Not found"}},
)
parentService = ParentService()

# 부모 생성
@router.post("/")
def create_parent(createParentInput: CreateParentInput)-> CreateParentOutput:
    parent = parentService.createParent(createParentInput)

    if parent is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Parent not found")

    parent_data = {
        'parent_id': parent.parent_id,
        'password': parent.password,
        'email': parent.email,
        'name': parent.name,
        'nickname': parent.nickname,
        'signInMethod': parent.signInMethod,
        'emailVerified': parent.emailVerified,
        'photoId': parent.photoId,
        'description': parent.description
    }

    return JSONResponse(status_code=201, content={
        'parent': parent_data,
        'x-jwt': signJWT(parent.parent_id)
    })

# 부모 정보 조회
@router.get("/", dependencies=[Depends(JWTBearer())])
def get_parent(parent_id: str = Depends(JWTBearer()))-> GetParentByEmailOutput:
    if parent_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")

    parent = parentService.getParentByEmail(parent_id)

    if parent is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Parent not found")
    
    parent_data = {
        'parent_id': parent.parent_id,
        'password': parent.password,
        'email': parent.email,
        'name': parent.name,
        'nickname': parent.nickname,
        'signInMethod': parent.signInMethod,
        'emailVerified': parent.emailVerified,
        'photoId': parent.photoId,
        'description': parent.description
    }

    return JSONResponse(status_code=200, content={
        'parent': parent_data,
        'x-jwt': signJWT(parent.parent_id)
    })

# 부모 정보 수정
@router.put("/", dependencies=[Depends(JWTBearer())])
def update_parent(updateParentInput: UpdateParentInput,
                   parent_id: str = Depends(JWTBearer())) -> UpdateParentOutput:
    if parent_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Parent not found")
    
    parent=parentService.updateParent(parent_id, updateParentInput)

    if parent is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Update failed")

    return {
        "success": 200 if parent else 403,
        "parent": parent
    }

# 부모 삭제
@router.delete("/", dependencies=[Depends(JWTBearer())])
def delete_parent(parent_id: str = Depends(JWTBearer())) -> DeleteParentOutput:
    if parent_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Parent not found")
    
    parent=parentService.deleteParent(parent_id)

    return {
        "success": 200 if parent else 403,
    }

# 이메일로 부모 목록 조회
@router.get("/friends")
def get_friends(emails: Optional[str] = None):

    email_list = emails.split(',') if emails is not None else []

    friends_dict = parentService.getFriends(email_list)

    return friends_dict


# 부모에게 다른 아기 pbconnect 요청
@router.post("/pbconnect")
def create_pbconnect(baby_id: str,parent_id: str = Depends(JWTBearer())) -> CreatePBConnectOutput:

    pbconnect = parentService.create_pbconnect(baby_id,parent_id)

    if pbconnect is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="PBConnect not found")

    return {
        "success": 200 if pbconnect else 403,
    }


# @router.get("/all")
# def get_parent():
#     parent = parentService.getParentAll()

#     return parent
