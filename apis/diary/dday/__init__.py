from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Header, Form
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer

from services.dday import DdayService
from schemas.dday import *
from error.exception.customerror import *

router = APIRouter(
    prefix="/dday",
    tags=["dday"],
    responses={404: {"description": "Not found"}},
)

ddayService = DdayService()


# DDay 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_dday(createDDayInput: CreateDDayInput,
                       parent_id: str = Depends(JWTBearer())) -> CreateDDayOutput:
    try:
        dday = ddayService.createDDay(parent_id, createDDayInput)
        print(dday)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create dday")
    return {'success': 200, 'message': 'Success to create dday', 'dday': dday}


# DDay 사진 업로드
@router.post("/photoUpload/{dday_id}", dependencies=[Depends(JWTBearer())])
async def upload_dday_photo(dday_id: int,
                         fileList: List[UploadFile],
                         parent_id: str = Depends(JWTBearer())) -> PhotoUploadOutput:
    try:
        photo = ddayService.uploadDDayPhoto(parent_id, dday_id, fileList)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to add dday image")
    return {'success': 200, 'message': 'Success to upload dday image'}


# 산모수첩에 대한 전체 DDay 조회
@router.get("/all/{diary_id}", dependencies=[Depends(JWTBearer())])
async def get_all_dday(diary_id: int,
                    parent_id: str = Depends(JWTBearer())) -> GetAllDDayOutput:
    try:
        dday = ddayService.getAllDDay(parent_id, diary_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get dday")
    return {'success': 200, 'message': 'Success to get dday', 'dday': dday}


# DDay 가져오기
@router.get("/{diary_id}/{create_time}", dependencies=[Depends(JWTBearer())])
async def get_one_dday(diary_id: int,
                    create_time: str,
                    parent_id: str = Depends(JWTBearer())) -> GetDDayOutput:
    try:
        create_time = datetime.strptime(create_time, "%Y-%m-%d")
        dday = ddayService.getOneDDay(parent_id, diary_id, create_time)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get dday")
    return {'success': 200, 'message': 'Success to get dday', 'dday': dday}


# DDay 수정
@router.put("/update", dependencies=[Depends(JWTBearer())])
async def update_dday(updateDDayInput: UpdateDDayInput,
                       parent_id: str = Depends(JWTBearer())) -> UpdateDDayOutput:
    try:
        dday = ddayService.updateDDay(parent_id, updateDDayInput)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to update dday")
    return {'success': 200, 'message': 'Success to update dday', 'dday': dday}


# DDay 사진 수정
@router.put("/photoUpdate/{dday_id}", dependencies=[Depends(JWTBearer())])
async def update_dday_photo(dday_id: int,
                         fileList: List[UploadFile],
                         parent_id: str = Depends(JWTBearer())) -> PhotoUploadOutput:
    try:
        photo = ddayService.updateDDayPhoto(parent_id, dday_id, fileList)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to update dday image")
    return {'success': 200, 'message': 'Success to update dday image'}


# DDay 삭제
@router.delete("/delete/{dday_id}", dependencies=[Depends(JWTBearer())])
async def delete_dday(dday_id: int,
                       parent_id: str = Depends(JWTBearer())) -> DeleteDDayOutput:
    try:
        dday = ddayService.deleteDDay(parent_id, dday_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete dday")
    return {'success': 200, 'message': 'Success to delete dday'}