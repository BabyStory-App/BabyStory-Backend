from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Header, Form
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer

from services.hospital import HospitalService
from schemas.hospital import *
from error.exception.customerror import *

router = APIRouter(
    prefix="/hospital",
    tags=["hospital"],
    responses={404: {"description": "Not found"}},
)

hospitalService = HospitalService()

# 산모수첩 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_hospital(createHospitalInput: CreateHospitalInput,
                           parent_id: str = Depends(JWTBearer())) -> CreateHospitalOutput:
    try:
        hospital = hospitalService.createHospital(parent_id, createHospitalInput)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create hospital")
    return {'success': 200, 'message': 'Success to create hospital', 'hospital': hospital}


# 다이어리에 대한 전체 산모수첩 조회
@router.post("/all", dependencies=[Depends(JWTBearer())])
async def get_all_hospital(getHospitalInput: GetHospitalInput,
                       parent_id: str = Depends(JWTBearer())) -> List[GetHospitalOutput]:
    try:
        hospitals = hospitalService.getAllHospital(parent_id, getHospitalInput)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get hospital")
    return {'success': 200, 'message': 'Success to get hospital', 'hospitals': hospitals}


# 하나의 산모수첩 조회
@router.post("/get/{hospital_id}", dependencies=[Depends(JWTBearer())])
async def get_hospital(hospital_id: int,
                       parent_id: str = Depends(JWTBearer())) -> GetHospitalOutput:
    try:
        hospital = hospitalService.getHospital(parent_id, hospital_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get hospital")
    return {'success': 200, 'message': 'Success to get hospital', 'hospital': hospital}


# 산모수첩 수정
@router.put("/update", dependencies=[Depends(JWTBearer())])
async def update_hospital(updateHospitalInput: UpdateHospitalInput,
                          parent_id: str = Depends(JWTBearer())) -> UpdateHospitalOutput:
    try:
        hospital = hospitalService.updateHospital(parent_id, updateHospitalInput)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to update hospital")
    return {'success': 200, 'message': 'Success to update hospital', 'hospital': hospital}


# 산모수첩 삭제
@router.delete("/delete/{hospital_id}", dependencies=[Depends(JWTBearer())])
async def delete_hospital(hospital_id: int, parent_id: str = Depends(JWTBearer())) -> DeleteHospitalOutput:
    try:
        hospital = hospitalService.deleteHospital(parent_id, hospital_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=str(error))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete hospital")
    return {'success': hospital, 'message': 'Success to delete hospital'}