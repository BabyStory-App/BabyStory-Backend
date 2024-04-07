from fastapi import APIRouter, HTTPException, UploadFile, Header, Depends, Form, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime
from constants.path import BABY_CRY_DATASET_DIR
from typing import Union, Optional, List
import os

from services.baby import BabyService
from auth.auth_bearer import JWTBearer


router = APIRouter(
    prefix="/baby",
    tags=["baby"],
    responses={404: {"description": "Not found"}},
)
babyService = BabyService()


@router.post("/create", dependencies=[Depends(JWTBearer())])
def create_baby():
    """
    input: 
        - JWT token -> parent_id
        - baby: (name, gender, birthDate, bloodType, imageFile)
    output:
        - sucess_code: int
        - baby: Baby
    process
        1. JWT -> 부모가 존재하는지 확인
        2. baby 생성
        3. 데이터베이스에 추가.
        4. 아기 반환
    """
    pass


@router.get("/", dependencies=[Depends(JWTBearer())])
def get_baby():
    pass


@router.put("/", dependencies=[Depends(JWTBearer())])
def update_baby():
    pass


@router.delete("/", dependencies=[Depends(JWTBearer())])
def delete_baby():
    pass


@router.get("/all", dependencies=[Depends(JWTBearer())])
def get_babies():
    pass
