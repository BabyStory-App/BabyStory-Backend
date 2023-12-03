from fastapi import APIRouter, HTTPException, UploadFile, Header, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime
from constants.path import *
from typing import Union, Optional
import os

router = APIRouter(
    prefix="/raws",
    tags=["raws"],
    responses={404: {"description": "Not found"}},
)

@router.get("/profile/{file_id}")
async def read_file(file_id: str):
    file_path = os.path.join(PROFILE_IMAGE_DIR, f'{file_id}.jpeg')
    print('searching file: ', file_path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    else:
        return FileResponse(os.path.join(ASSET_DIR, 'default_profile_image.jpeg'))