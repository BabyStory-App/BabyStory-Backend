from fastapi import APIRouter, HTTPException, UploadFile, Header
from fastapi.responses import JSONResponse, FileResponse
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime
from constants.path import BABY_CRY_DATASET_DIR
from typing import Union, Optional
import os

from schemas.parent import ParentCreateInput, ParentType
from services.parent import ParentService
from model.parent import Parent


router = APIRouter(
    prefix="/parent",
    tags=["parent"],
    responses={404: {"description": "Not found"}},
)
parentService = ParentService()

"""
TODO:
- create a new user: / (POST) (uid, nickname, email) (return uid)

- get user info: / (GET) (uid) (return nickname, email)

- update user info: / (PUT) (uid, nickname, email) (return uid)

- delete user: / (DELETE) (uid) (return uid)
"""


@router.post("/", response_model=ParentType)
def create_parent(parent_input: ParentCreateInput):
    parent = parentService.create_parent(parent_input)
    if parent is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create parent")
    return parent


@router.get("/", response_model=Optional[ParentType])
async def get_parent(uid: Union[str, None] = Header(default=None)):
    if uid is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="uid is required")

    return parentService.get_parent(uid)
