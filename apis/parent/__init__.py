from fastapi import APIRouter, HTTPException, UploadFile, Header, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime
from constants.path import BABY_CRY_DATASET_DIR
from typing import Union, Optional
import os

from schemas.parent import ParentCreateInput, ParentType, ParentUpdateInput
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
def create_parent(parent_input: ParentCreateInput):
    parent = parentService.create_parent(parent_input)
    if type(parent) == str:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=parent)
    return JSONResponse(status_code=201, content={
        'parent': jsonable_encoder(parent),
        'x-jwt': signJWT(parent.uid)
    })


@router.get("/", response_model=Optional[ParentType])
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


@router.put("/", dependencies=[Depends(JWTBearer())])
def update_parent(parent_input: ParentUpdateInput, uid: str = Depends(JWTBearer())):
    parent = parentService.update_parent(uid, parent_input)
    if type(parent) == str:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=parent)

    return parent


@router.delete("/", dependencies=[Depends(JWTBearer())])
def delete_parent(uid: str = Depends(JWTBearer())) -> bool:
    return parentService.delete_parent(uid)
