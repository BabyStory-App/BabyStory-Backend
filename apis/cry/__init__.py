from fastapi import APIRouter, HTTPException, UploadFile, Header, Depends
from fastapi.responses import JSONResponse, FileResponse
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime
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


@router.post("/predict", dependencies=[Depends(JWTBearer())])
async def upload_file(
        file: UploadFile = None,
        uid: str = Depends(JWTBearer()),
        baby_id: Union[str, None] = Header(default=None)):
    # return JSONResponse(content={
    #     "time": "2023-11-15 14:07:48",
    #     "filename": "sample_file.wav",
    #     'predictMap': {
    #             "hug": 0.860338930413126945,
    #             "sad": 0.05292745303362608,
    #             "diaper": 0.0019440052565187216,
    #             "sleepy": 0.0081116771697998,
    #             "hungry": 0.00332592040300369,
    #             "awake": 0.06723734736442566,
    #             "uncomfortable": 0.01611471176147461,
    #     },
    #     "intensity": 'medium',
    #     'audioURL': "20231115-140748",
    # })

    if baby_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="baby id not provided")

    if file == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="File not provided")

    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Only .wav files are accepted")

    predict_result = await cryService.predict(file, uid)

    return JSONResponse(content={"babyId": baby_id, **predict_result})


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
    start_date = end_date.replace(month=end_date.month-1)

    inspect_result = await cryService.inspect(baby_id, start_date, end_date)

    return JSONResponse(content={"babyId": baby_id})
