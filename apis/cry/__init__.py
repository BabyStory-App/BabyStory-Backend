from fastapi import APIRouter, HTTPException, UploadFile, Header, Depends, Form
from fastapi.responses import JSONResponse, FileResponse
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime, timedelta
from constants.path import BABY_CRY_DATASET_DIR
from typing import Union, Optional, List
import os

from auth.auth_bearer import JWTBearer
from services.cry import CryService


router = APIRouter(
    prefix="/cry",
    tags=["cry"],
    responses={404: {"description": "Not found"}},
)
cryService = CryService()


@router.get("/all", dependencies=[Depends(JWTBearer())])
async def get_crys():
    pass


@router.post("/predict", dependencies=[Depends(JWTBearer())])
async def upload_file(
        file: Optional[UploadFile] = None,
        uid: str = Depends(JWTBearer()),
        # babyId: Optional[str] = Form(...)
):

    if uid == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="baby id not provided")

    if file == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="File not provided")

    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Only .wav files are accepted")

    predict_result = await cryService.predict(file, uid)
    if predict_result == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Failed to predict")

    return predict_result


@router.post("/predict_test")
async def upload_file(file: Optional[UploadFile] = None):
    try:
        if file == None:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail="File not provided")

        if not file.filename.endswith(".wav"):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail="Only .wav files are accepted")

        predict_result = await cryService.just_predict(file)

        if predict_result == None:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                                detail="Failed to predict")

        return predict_result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Failed to predict")


@router.get("/inspect", dependencies=[Depends(JWTBearer())])
async def inspect(
        babyId: str = Header(None),
        uid: str = Depends(JWTBearer())):

    if babyId is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="baby id not provided")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    inspect_result = await cryService.inspect(babyId, start_date, end_date)

    return JSONResponse(content=inspect_result)


@router.get("/duration/update", dependencies=[Depends(JWTBearer())])
async def update_duration(
        audio_id: str = Header(None),
        duration: float = Header(0.0),
        uid: str = Depends(JWTBearer())):

    if audio_id is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Audio id not provided")

    update_result = await cryService.update_duration(audio_id, duration)
    if type(update_result) == str:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail=update_result)

    return update_result
