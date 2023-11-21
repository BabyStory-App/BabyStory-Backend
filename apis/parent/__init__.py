from fastapi import APIRouter, HTTPException, UploadFile, Header
from fastapi.responses import JSONResponse, FileResponse
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime
from constants.path import BABY_CRY_DATASET_DIR
import os

from schemas.parent import ParentCreateInput
from services.parent import ParentService


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


@router.post("/", response_model=None)
async def create_new_user(parent):
    parentService.create_parent(parent)
    return JSONResponse(status_code=200)
