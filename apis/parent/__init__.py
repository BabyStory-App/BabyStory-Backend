from fastapi import APIRouter, HTTPException, UploadFile, Header, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime
from constants.path import BABY_CRY_DATASET_DIR
from typing import Union, Optional
import os

from services.parent import ParentService
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer
from schemas.parent import *


router = APIRouter(
    prefix="/parent",
    tags=["parent"],
    responses={404: {"description": "Not found"}},
)
parentService = ParentService()


@router.post("/")
def create_parent(parent_input: CreateParentInput):
    parent = parentService.createParent(parent_input)

    if parent is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Parent not found")

    return JSONResponse(status_code=201, content={
        'parent': parent,
        'x-jwt': signJWT(parent.parent_id)
    })


@router.get("/", dependencies=[Depends(JWTBearer())])
def get_parent(uid: str = Depends(JWTBearer())):
    if uid is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="uid is required")

    parent = parentService.getParentByEmail(uid)
    if parent is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Parent not found")

    return JSONResponse(status_code=200, content={
        'parent': parent,
        'x-jwt': signJWT(parent.parent_id)
    })


@router.put("/", dependencies=[Depends(JWTBearer())])
def update_parent(parent_input: UpdateParentInput, uid: str = Depends(JWTBearer())) -> bool:
    if uid is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="correct id require")
    return parentService.updateParent(uid, parent_input)


@router.delete("/", dependencies=[Depends(JWTBearer())])
def delete_parent(uid: str = Depends(JWTBearer())) -> bool:
    if uid is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="correct id require")
    return parentService.deleteParent(uid)


@router.get("/friends")
def get_friends(emails: Optional[str] = None):

    email_list = emails.split(',') if emails is not None else []

    friends_dict = parentService.getFriends(email_list)

    return friends_dict


# @router.get("/all")
# def get_parent():
#     parent = parentService.getParentAll()

#     return parent
