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


def search_filename(file_id: str, dir_path: str):
    try:
        # 디렉토리 내의 파일들 검색
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            # 파일인지 확인
            if os.path.isfile(file_path):
                # 확장자 분리
                name, _ = os.path.splitext(filename)
                # 이름이 file_id와 일치하면 해당 파일 반환
                if name == file_id:
                    return file_path
    except Exception as e:
        return None


def get_image_path(file_id: str, search_in_dir: str):
    if file_id == None:
        return None

    # 파일이 저장된 디렉토리 경로
    file_id = file_id.split('.')[0] if '.' in file_id else file_id
    dir_path = search_in_dir

    # 디렉토리가 존재하지 않으면 기본 이미지 반환
    if not os.path.isdir(dir_path):
        return None

    return search_filename(file_id, dir_path)


@router.get("/profile/{file_id}")
async def read_file(file_id: str):
    file_path = get_image_path(file_id, PROFILE_IMAGE_DIR)
    if file_path != None:
        return FileResponse(file_path)
    else:
        return FileResponse(os.path.join(ASSET_DIR, 'default_profile_image.jpeg'))


@router.get("/baby/profile/{file_id}")
async def read_file(file_id: str):
    file_path = get_image_path(file_id, BABY_PROFILE_DIR)
    if file_path != None:
        return FileResponse(file_path)
    else:
        return FileResponse(os.path.join(ASSET_DIR, 'default_profile_image.jpeg'))


@router.get("/post/photo/{file_id}")
async def read_file(file_id: str):
    file_id = f'{file_id}-1' if file_id.find('-') == -1 else file_id
    file_path = get_image_path(file_id, os.path.join(
        POST_PHOTO_DIR, file_id.split('-')[0]))
    if file_path != None:
        return FileResponse(file_path)
    else:
        return FileResponse(os.path.join(POST_PHOTO_DIR, 'default_post_image.jpeg'))


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
