from fastapi import APIRouter, HTTPException, UploadFile, Header
from fastapi.responses import JSONResponse, FileResponse
from starlette.status import HTTP_400_BAD_REQUEST
from datetime import datetime
from constants.path import BABY_CRY_DATASET_DIR
import os

from services.cry_predict import cry_predict


router = APIRouter(
    prefix="/baby",
    tags=["baby"],
    responses={404: {"description": "Not found"}},
)


# http://localhost:8000/baby/predict
@router.post("/predict")
async def upload_file(file: UploadFile = None, uid: str = Header(None)):
    return JSONResponse(content={
        "time": "2023-11-15 14:07:48",
        "filename": "sample_file.wav",
        'predictMap': {
                "diaper": 0.7981116771697998,
                "hungry": 0.09332592040300369,
                "awake": 0.06723734736442566,
                "uncomfortable": 0.01611471176147461,
                "sad": 0.01292745303362608,
                "hug": 0.010338930413126945,
                "sleepy": 0.0019440052565187216
        },
        "intensity": 'medium',
        'audioURL': "20231115-140748",
    })
    # print(f'uid: {uid}')
    # if uid == None:
    #     raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
    #                         detail="uid not provided")
    uid = "test_user_id"

    if file == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="File not provided")

    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Only .wav files are accepted")

    print(f"Get file: {file.filename}")
    content = await file.read()

    curtime = datetime.now()
    timestamp = curtime.strftime("%Y%m%d-%H%M%S")
    save_filename = f"{uid}_{timestamp}.wav"
    file_path = os.path.join(BABY_CRY_DATASET_DIR, save_filename)
    with open(file_path, 'wb') as f:
        f.write(content)

    # get predictMap
    print(f'response state:')
    predictMap = await cry_predict(content)
    for key in predictMap:
        print(f'{key}: {predictMap[key]}')

    return JSONResponse(content={
        "time": curtime.strftime("%Y-%m-%d %H:%M:%S"),
        "filename": file.filename,
        'predictMap': predictMap,
        "intensity": 'medium',
        'audioURL': timestamp,
    })
# {
# 	"time": "2023-11-13 13:22:41",
# 	"filename": "babycry_diaper.wav",
# 	"predictMap": {
# 		"diaper": 0.7981116771697998,
# 		"hungry": 0.09332592040300369,
# 		"awake": 0.06723734736442566,
# 		"uncomfortable": 0.01611471176147461,
# 		"sad": 0.01292745303362608,
# 		"hug": 0.010338930413126945,
# 		"sleepy": 0.0019440052565187216
# 	},
# 	"intensity": "medium",
# 	"audioURL": "audio_path"
# }


@router.get("/wav")
async def get_file(uid: str = Header(None), audioId: str = Header(None)):
    if uid is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="uid not provided")

    if audioId is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="audioId not provided")

    file_path = os.path.join(BABY_CRY_DATASET_DIR, f'{uid}_{audioId}.wav')

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Return the file
    return FileResponse(file_path)
