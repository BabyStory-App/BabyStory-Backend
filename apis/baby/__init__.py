from fastapi import APIRouter, HTTPException, UploadFile, Header, Depends, Form, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime
from constants.path import BABY_CRY_DATASET_DIR
from typing import Union, Optional, List
import os

from services.baby import BabyService
from schemas.baby import *
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer


router = APIRouter(
    prefix="/baby",
    tags=["baby"],
    responses={404: {"description": "Not found"}},
)
babyService = BabyService()


# 아기 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_baby(create_baby_request: create_baby_input,
                      parent_id: str = Depends(JWTBearer())) -> create_baby_output:
    if parent_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Invalid parent_id")

    baby = babyService.create_baby(parent_id, create_baby_request)

    return JSONResponse(status_code=200, content={
        'baby': baby
    })


# 아기 정보 수정
@router.put("/", dependencies=[Depends(JWTBearer())])
def update_baby(update_baby_input: update_baby_input,
                parent_id: str = Depends(JWTBearer())) -> update_baby_output:
    if update_baby_input.baby_id != baby_id:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Invalid baby_id")
    baby = babyService.update_baby(baby_id, update_baby_input)
    if baby is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Invalid baby_id")
    return {
        "success": True if baby else False,
        "baby_id": baby
    }

# 아기 삭제


@router.delete("/", dependencies=[Depends(JWTBearer())])
def delete_baby(delete_baby_input: delete_baby_input,
                parent_id: str = Depends(JWTBearer())) -> delete_baby_output:
    if parent_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Invalid parent_id")

    success = babyService.delete_baby(parent_id, delete_baby_input.baby_id)

    return {
        "success": 200 if success else 403,
    }


@router.get("/all", dependencies=[Depends(JWTBearer())])
def get_babies():
    pass
