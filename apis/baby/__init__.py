from fastapi import APIRouter, HTTPException, UploadFile, Depends, Form
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer
from services.baby import BabyService
from schemas.baby import *
from error.exception.customerror import *

router = APIRouter(
    prefix="/baby",
    tags=["baby"],
    responses={404: {"description": "Not found"}},
)
babyService = BabyService()


# 아기 관리
@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_baby(createBabyInput: CreateBabyInput, parent_id: str = Depends(JWTBearer())) -> CreateBabyOutput:
    try:
        # 아기 생성
        baby = babyService.createBaby(createBabyInput)
        # 아기-부모 연결 생성
        pbconnect = babyService.createPbconnect(parent_id, baby.baby_id)

    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create baby")
    return {'baby': baby}


# 아기 프로필 사진 업로드
@router.post("/photoUpload", dependencies=[Depends(JWTBearer())])
async def upload_baby_ProfileImag(file: Optional[UploadFile] = None, baby_id: str = Form(...),
                                  parent_id: str = Depends(JWTBearer())) -> uploadProfileImageOutput:
    try:
        success = babyService.uploadProfileImage(file, baby_id, parent_id)
        if success == False:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="pbconnect not found")
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to upload photo")
    return {
        "success": 200 if success else 403,
        "photoId": baby_id
    }


# 아기 정보 조회
@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_baby(parent_id: str = Depends(JWTBearer())):
    try:
        baby = babyService.getBaby(parent_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get baby")
    return {'baby': baby}


# 아기 정보 수정
@router.put("/update", dependencies=[Depends(JWTBearer())])
async def update_baby(updateBabyInput: UpdateBabyInput, parent_id: str = Depends(JWTBearer())) -> UpdateBabyOutput:
    try:
        baby = babyService.updateBaby(updateBabyInput, parent_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to update baby")
    return {"success": 200 if baby else 403, 'baby': baby}


# 아기 삭제
@router.delete("/delete/{baby_id}", dependencies=[Depends(JWTBearer())])
async def delete_baby(baby_id: str, parent_id: str = Depends(JWTBearer())) -> DeleteBabyOutput:
    try:
        success = babyService.deleteBaby(baby_id, parent_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to delete baby")
    return {"success": 200 if success else 403}
