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


@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_baby(createBabyInput: CreateBabyInput, parent_id: str = Depends(JWTBearer())) -> CreateBabyOutput:
    '''
    아기 생성
    --input
        - createBabyInput: 아기 정보
    --output
        - Baby: 아기 정보
    '''
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


@router.post("/photoUpload", dependencies=[Depends(JWTBearer())])
async def upload_baby_ProfileImag(file: Optional[UploadFile] = None,
                                  baby_id: int = Form(...),
                                  parent_id: str = Depends(JWTBearer())) -> uploadProfileImageOutput:
    '''
    생성된 아기 사진 업로드
    --input
        - file: 업로드할 파일
        - baby_id: 아기 아이디
        - parent_id: 부모 아이디
    --output
        - success: 업로드 성공 여부
        - photoId: 사진 아이디
    '''
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


@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_baby(parent_id: str = Depends(JWTBearer())):
    '''
    아기 정보 가져오기
    --input
        - parent_id: 부모 아이디
    --output
        - Baby: 아기 정보
    '''
    try:
        baby = babyService.getBaby(parent_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get baby")
    return {'baby': baby}


@router.put("/", dependencies=[Depends(JWTBearer())])
async def update_baby(updateBabyInput: UpdateBabyInput, parent_id: str = Depends(JWTBearer())) -> UpdateBabyOutput:
    '''
    아기 정보 수정
    --input
        - updateBabyInput: 수정할 아기 정보
        - parent_id: 부모 아이디
    --output
        - Baby: 수정된 아기 정보
    '''
    try:
        baby = babyService.updateBaby(updateBabyInput, parent_id)
    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to update baby")
    return {"success": 200 if baby else 403, 'baby': baby}


@router.delete("/", dependencies=[Depends(JWTBearer())])
async def delete_baby(baby_id: str, parent_id: str = Depends(JWTBearer())) -> DeleteBabyOutput:
    '''
    아기 삭제
    --input
        - baby_id: 삭제할 아기 아이디
        - parent_id: 부모 아이디
    --output
        - success: 삭제 성공 여부
    '''
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
