from fastapi import APIRouter, HTTPException, UploadFile, Header, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime
from constants.path import *
from typing import Union, Optional
import os

from auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/raws",
    tags=["raws"],
    responses={404: {"description": "Not found"}},
)


@router.get("/profile/{file_id}")
async def read_file(file_id: str):
    file_path = os.path.join(PROFILE_IMAGE_DIR, f'{file_id}.jpeg')
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    else:
        return FileResponse(os.path.join(ASSET_DIR, 'default_profile_image.jpeg'))


@router.get("/baby/profile/{file_id}")
async def read_file(file_id: str):
    file_path = os.path.join(BABY_PROFILE_DIR, f'{file_id}.jpeg')
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    else:
        return FileResponse(os.path.join(ASSET_DIR, 'default_profile_image.jpeg'))


@router.get("/cry/{audioId}")
async def get_file(audioId: str):

    if audioId is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="audioId not provided")

    file_path = os.path.join(BABY_CRY_DATASET_DIR, f'{uid}_{audioId}.wav')

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Return the file
    return FileResponse(file_path)
