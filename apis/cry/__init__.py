from fastapi import APIRouter, HTTPException, UploadFile, Header, Depends
from fastapi.responses import JSONResponse, FileResponse
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime, timedelta
from constants.path import BABY_CRY_DATASET_DIR
from typing import Union, Optional, List
import os

from auth.auth_bearer import JWTBearer
from services.cry import CryService
from utils import process_str_date
from model.types.cry_state import CryStateType


router = APIRouter(
    prefix="/cry",
    tags=["cry"],
    responses={404: {"description": "Not found"}},
)
cryService = CryService()

@router.get("/",response_model=List[CryStateType], dependencies=[Depends(JWTBearer())])
async def get_crys(
        start: Optional[str] = None,
        end: Optional[str] = None,
        baby_id: str = Header(None),
        uid: str = Depends(JWTBearer())):

    if baby_id is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="baby id not provided")
    
    date_obj = process_str_date(start, end)
    if type(date_obj) == str:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail=date_obj)
    
    crys = await cryService.get_crys(baby_id, date_obj[0], date_obj[1])

    return crys

@router.post("/predict", dependencies=[Depends(JWTBearer())])
async def upload_file(
        file: UploadFile = None,
        uid: str = Depends(JWTBearer()),
        baby_id: Union[str, None] = Header(default=None)):
    if baby_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="baby id not provided")

    if file == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="File not provided")

    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Only .wav files are accepted")

    predict_result = await cryService.predict(file, uid, baby_id)
    if predict_result == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Failed to predict")

    return predict_result


@router.get("/wav", dependencies=[Depends(JWTBearer())])
async def get_file(
        uid: str = Depends(JWTBearer()),
        audioId: str = Header(None)):

    if audioId is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="audioId not provided")

    file_path = os.path.join(BABY_CRY_DATASET_DIR, f'{uid}_{audioId}.wav')

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Return the file
    return FileResponse(file_path)


@router.get("/inspect", dependencies=[Depends(JWTBearer())])
async def inspect(
        baby_id: str = Header(None),
        uid: str = Depends(JWTBearer())):

    if baby_id is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="baby id not provided")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    inspect_result = await cryService.inspect(baby_id, start_date, end_date)

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

