from fastapi import APIRouter, HTTPException, UploadFile, Header
from fastapi.responses import JSONResponse, FileResponse
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime
from constants.path import BABY_CRY_DATASET_DIR
from typing import Union, Optional
import os

from schemas.baby import BabyCreateInput, BabyType, BabyUpdateInput
from services.baby import BabyService
from model.baby import Baby


router = APIRouter(
    prefix="/baby",
    tags=["baby"],
    responses={404: {"description": "Not found"}},
)
babyService = BabyService()


@router.post("/", response_model=BabyType)
def create_baby(baby_input: BabyCreateInput):
    baby = babyService.create_baby(baby_input)
    if type(baby) == str:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=baby)
    return baby


@router.get("/", response_model=Optional[BabyType])
def get_baby(uid: Union[str, None] = Header(default=None)):
    if uid is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="uid is required")

    return babyService.get_baby(uid)


@router.put("/", response_model=BabyType)
def update_baby(baby_input: BabyUpdateInput, uid: Union[str, None] = Header(default=None)):
    if uid is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="uid is required")

    baby = babyService.update_baby(uid, baby_input)
    if type(baby) == str:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=baby)

    return baby


@router.delete("/")
def delete_baby(uid: Union[str, None] = Header(default=None)) -> bool:
    if uid is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="uid is required")

    return babyService.delete_baby(uid)


"""
문제 정의
누군가 uid를 가져와 다른 사람의 정보를 수정할 수 있다.
* jwt를 활용하면 본인인지는 확인할 수 있으나 
"""
