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