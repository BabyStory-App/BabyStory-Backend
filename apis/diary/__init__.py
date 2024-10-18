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
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
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
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to upload diary cover image")
    return {'success': success, 'message': 'Success to upload diary cover image'}


# 아기의 모든 다이어리 가져오기
@router.get("/{baby_id}", dependencies=[Depends(JWTBearer())])
async def get_all_diary(baby_id: str,
                        parent_id: str = Depends(JWTBearer())) -> GetDiaryOutput:
    try:
        diary = diaryService.getAllDiary(parent_id, baby_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get all diary")
    return {"success": 200, "message": "Success to get all diary", "diary": diary}


# 하나의 다이어리 가져오기
@router.get("/get/{diary_id}", dependencies=[Depends(JWTBearer())])
async def get_diary(diary_id: int,
                    parent_id: str = Depends(JWTBearer())) -> GetDiaryOutput:
    try:
        diary = diaryService.getDiary(parent_id, diary_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get diary")
    return {"success": 200, "message": "Success to get diary", "diary": diary}


# 다이어리 수정
@router.put("/update", dependencies=[Depends(JWTBearer())])
async def update_diary(updateDiaryInput: UpdateDiaryInput,
                       parent_id: str = Depends(JWTBearer())) -> UpdateDiaryOutput:
    try:
        diary = diaryService.updateDiary(parent_id, updateDiaryInput)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to update diary")
    return {"success": 200, "message": "Success to update diary", "diary": diary}


# 다이어리 표지 사진 수정
@router.put("/updateCover/{diary_id}", dependencies=[Depends(JWTBearer())])
async def update_diary_cover_image(file: UploadFile,
                                      diary_id: int,
                                      parent_id: str = Depends(JWTBearer())) -> UploadDiaryCoverOutput:
     try:
          success = diaryService.updateDiaryCover(parent_id, file, diary_id)
     except CustomException as error:
          raise HTTPException(
                status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
     except Exception as e:
          raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Failed to update diary cover image")
     return {'success': success, 'message': 'Success to update diary cover image'}


# 다이어리 삭제
@router.delete("/delete/{diary_id}", dependencies=[Depends(JWTBearer())])
async def delete_diary(diary_id: int,
                       parent_id: str = Depends(JWTBearer())) -> DeleteDiaryOutput:
    try:
        success = diaryService.deleteDiary(parent_id, diary_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete diary")
    return {"success": success, "message": "Success to delete diary"}