from fastapi import APIRouter, HTTPException, UploadFile, Header, Depends, Form, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime
from constants.path import BABY_CRY_DATASET_DIR
from typing import Union, Optional, List
import os

from model.baby import Baby
from schemas.baby import BabyCreateInput, BabyUpdateInput
from model.types.baby import BabyType
from services.baby import BabyService
from auth.auth_bearer import JWTBearer

from pydantic import BaseModel


router = APIRouter(
    prefix="/baby",
    tags=["baby"],
    responses={404: {"description": "Not found"}},
)
babyService = BabyService()


@router.post("/create", dependencies=[Depends(JWTBearer())])
def create_baby(
        name: str = Form(...),
        birthDate: str = Form(...),
        gender: str = Form(...),
        bloodType: str = Form(...),
        file: UploadFile = File(...),
        uid: str = Depends(JWTBearer())):
    inputBaby = BabyCreateInput(
        name=name,
        birthDate=datetime.strptime(birthDate, "%Y-%m-%dT%H:%M:%S.%f"),
        gender=gender,
        bloodType=bloodType
    )
    baby = babyService.create_baby(uid, inputBaby, file)
    if type(baby) == str:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=baby)
    return baby


@router.get("/", response_model=BabyType, dependencies=[Depends(JWTBearer())])
def get_baby(
        uid: str = Depends(JWTBearer()),
        baby_id: Union[str, None] = Header(default=None)):

    if baby_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="baby_id is required")
    baby = babyService.get_baby(uid, baby_id)
    if type(baby) == str:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=baby)

    return baby


@router.put("/", response_model=BabyType, dependencies=[Depends(JWTBearer())])
def update_baby(
        baby_input: BabyUpdateInput,
        uid: str = Depends(JWTBearer())):

    baby = babyService.update_baby(uid, baby_input)
    if type(baby) == str:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=baby)

    return baby


@router.delete("/", dependencies=[Depends(JWTBearer())])
def delete_baby(
        uid: str = Depends(JWTBearer()),
        baby_id: Union[str, None] = Header(default=None)):
    if baby_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="baby_id is required")
    return babyService.delete_baby(uid, baby_id)


@router.get("/all", response_model=List[BabyType], dependencies=[Depends(JWTBearer())])
def get_babies(
        uid: str = Depends(JWTBearer())):
    babies = babyService.get_babies(uid)
    if type(babies) == str:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=babies)
    return babies
