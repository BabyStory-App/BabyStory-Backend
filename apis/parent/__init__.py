from fastapi import APIRouter, HTTPException, UploadFile, Header
from fastapi.responses import JSONResponse, FileResponse
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime
from constants.path import BABY_CRY_DATASET_DIR
from typing import Union, Optional
import os

from schemas.parent import ParentCreateInput, ParentType, ParentUpdateInput
from services.parent import ParentService
from model.parent import Parent


router = APIRouter(
    prefix="/parent",
    tags=["parent"],
    responses={404: {"description": "Not found"}},
)
parentService = ParentService()


@router.post("/", response_model=ParentType)
def create_parent(parent_input: ParentCreateInput):
    parent = parentService.create_parent(parent_input)
    if type(parent) == str:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=parent)
    return parent


@router.get("/", response_model=Optional[ParentType])
def get_parent(uid: Union[str, None] = Header(default=None)):
    if uid is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="uid is required")

    return parentService.get_parent(uid)


@router.put("/", response_model=ParentType)
def update_parent(parent_input: ParentUpdateInput, uid: Union[str, None] = Header(default=None)):
    if uid is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="uid is required")

    parent = parentService.update_parent(uid, parent_input)
    if type(parent) == str:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=parent)

    return parent


@router.delete("/")
def delete_parent(uid: Union[str, None] = Header(default=None)) -> bool:
    if uid is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="uid is required")

    return parentService.delete_parent(uid)
