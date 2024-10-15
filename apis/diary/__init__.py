from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Header, Form
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer

from services.diary import DiaryService
from schemas.diary import *
from error.exception.customerror import *

router = APIRouter(
    prefix="/diary",
    tags=["diary"],
    responses={404: {"description": "Not found"}},
)

diaryService = DiaryService()


# 다이어리 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_diary(createDiaryInput: CreateDiaryInput,
                       parent_id: str = Depends(JWTBearer())) -> CreateDiaryOutput:
    try:
        diary = diaryService.createDiary(parent_id, createDiaryInput)
        print(diary)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create diary")
    return {'success': 200, 'message': 'Success to create diary', 'diary': diary}


# 다이어리 표지 사진 업로드
@router.post("/upload/{diary_id}", dependencies=[Depends(JWTBearer())])
async def upload_diary_cover_image(file: UploadFile,
                                   diary_id: int,
                                   parent_id: str = Depends(JWTBearer())) -> UploadDiaryCoverOutput:
    try:
        success = diaryService.uploadDiaryCover(parent_id, file, diary_id)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to upload diary cover image")
    return {'success': success, 'message': 'Success to upload diary cover image'}
