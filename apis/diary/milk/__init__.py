from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Header, Form
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer

from services.milk import MilkService
from schemas.milk import *
from error.exception.customerror import *

router = APIRouter(
    prefix="/milk",
    tags=["milk"],
    responses={404: {"description": "Not found"}},
)

milkService = MilkService()

# 수유일지 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_milk(createMilkInput: CreateMilkInput,
                      parent_id: str = Depends(JWTBearer())) -> CreateMilkOutput:
    try:
        milk = milkService.createMilk(parent_id, createMilkInput)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create milk")
    return {'success': 200, 'message': 'Success to create milk', 'milk': milk}


# 다이어리에 대한 전체 수유일지 조회
@router.get("/{diary_id}", dependencies=[Depends(JWTBearer())])
async def get_all_milk(diary_id: int,
                       parent_id: str = Depends(JWTBearer())) -> GetAllMilkOutput:
    try:
        milks = milkService.getAllMilk(parent_id, diary_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get milk")
    return {'success': 200, 'message': 'Success to get milk', 'milks': milks}


# 해당 날짜의 모든 수유일지 조회
@router.get("/{diary_id}/{mtime}", dependencies=[Depends(JWTBearer())])
async def get_milk(diary_id: int,
                   mtime: str,
                   parent_id: str = Depends(JWTBearer())) -> GetMilkOutput:
    try:
        milks = milkService.getMilk(parent_id, diary_id, mtime)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get milk")
    return {'success': 200, 'message': 'Success to get milk', 'milks': milks}


# 시작 날짜부터 끝 날짜까지의 수유일지 조회
@router.get("/{diary_id}/{start_time}/{end_time}", dependencies=[Depends(JWTBearer())])
async def get_milk_range(diary_id: int,
                         start_time: str,
                         end_time: str,
                         parent_id: str = Depends(JWTBearer())) -> GetMilkRangeOutput:
    try:
        milks = milkService.getMilkRange(
            parent_id, diary_id, start_time, end_time)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get milk")
    return {'success': 200, 'message': 'Success to get milk', 'milks': milks}


# 수유일지 수정
@router.put("/update", dependencies=[Depends(JWTBearer())])
async def update_milk(UpdateMilkInput: UpdateMilkInput,
                      parent_id: str = Depends(JWTBearer())) -> UpdateMilkOutput:
    try:
        milk = milkService.updateMilk(parent_id, UpdateMilkInput)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to update milk")
    return {'success': 200, 'message': 'Success to update milk', 'milk': milk}


# 수유일지 삭제
@router.delete("/delete/{milk_id}", dependencies=[Depends(JWTBearer())])
async def delete_milk(milk_id: int, parent_id: str = Depends(JWTBearer())) -> DeleteMilkOutput:
    try:
        milk = milkService.deleteMilk(parent_id, milk_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete milk")
    return {'success': 200, 'message': 'Success to delete milk'}
