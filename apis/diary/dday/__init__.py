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


# DDay 사진 추가
@router.post("/photoUpload/{dday_id}", dependencies=[Depends(JWTBearer())])
async def add_dday_image(dday_id: int,
                         fileList: List[UploadFile],
                         parent_id: str = Depends(JWTBearer())) -> UploadImageOutput:
    try:
        ddayImage = ddayService.addDDayImage(parent_id, dday_id, fileList)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to add dday image")
    return {'success': ddayImage}


# DDay 가져오기
@router.get("/{diary_id}/{create_time}", dependencies=[Depends(JWTBearer())])
async def get_dday(diary_id: int,
                    create_time: str,
                    parent_id: str = Depends(JWTBearer())) -> GetDDayOutput:
    try:
        create_time = datetime.strptime(create_time, "%Y-%m-%d")
        dday = ddayService.getDDay(parent_id, diary_id, create_time)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get dday")
    return {'success': 200, 'message': 'Success to get dday', 'dday': dday}