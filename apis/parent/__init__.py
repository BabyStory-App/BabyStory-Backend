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


router = APIRouter(
    prefix="/parent",
    tags=["parent"],
    responses={404: {"description": "Not found"}},
)
parentService = ParentService()


@router.post("/")
def create_parent():
    pass


@router.get("/")
def get_parent(uid: Union[str, None] = Header(default=None)):
    if uid is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="uid is required")

    parent = parentService.get_parent(uid)
    if parent is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Parent not found")

    return JSONResponse(status_code=200, content={
        'parent': jsonable_encoder(parent),
        'x-jwt': signJWT(parent.uid)
    })


@router.get("/friends")
def get_friends(emails: Optional[str] = None):
    # 이메일 리스트를 받아서 해당하는 친구들을 반환
    # 친구의 정보를 가져오는 것이기에 민감한 정보들은 제외하고 가져온다.
    email_list = emails.split(',') if emails is not None else []
    pass


@router.put("/", dependencies=[Depends(JWTBearer())])
def update_parent():
    pass


@router.delete("/", dependencies=[Depends(JWTBearer())])
def delete_parent(uid: str = Depends(JWTBearer())) -> bool:
    return parentService.delete_parent(uid)
