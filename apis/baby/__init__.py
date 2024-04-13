from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from auth.auth_bearer import JWTBearer

from services.baby import BabyService

from schemas.baby import *



router = APIRouter(
    prefix="/baby",
    tags=["baby"],
    responses={404: {"description": "Not found"}},
)
babyService = BabyService()


# 아기 생성
@router.post("/create", dependencies=[Depends(JWTBearer())])
def create_baby(createBabyInput: CreateBabyInput,
                parent_id: str = Depends(JWTBearer()))-> CreateBabyOutput:
    # 아기 생성
    baby = babyService.createBaby(createBabyInput)

    if baby is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Baby not found")
    
    # 아기-부모 연결 생성
    pbconnect = babyService.createPbconnect(parent_id,createBabyInput.baby_id)

    if pbconnect is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="PBConnect not found")
    
    return { 'baby': baby }



@router.get("/", dependencies=[Depends(JWTBearer())])
def get_baby(parent_id: str = Depends(JWTBearer())):
    # 부모 아이디가 없으면 에러
    if parent_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")
    
    # 아기 정보 가져오기
    baby = babyService.getBaby(parent_id)

    if baby is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="baby not found")
    
    return baby


# 아기 정보 수정
@router.put("/", dependencies=[Depends(JWTBearer())])
def update_baby(updateBabyInput: UpdateBabyInput,
                parent_id:str = Depends(JWTBearer())) -> UpdateBabyOutput:
    # 부모 아이디가 없으면 에러
    if parent_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid parent_id")

    # 아기 정보 수정
    baby = babyService.updateBaby(updateBabyInput,parent_id)

    if baby is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="baby not found")
    
    return{
        "success": 200 if baby else 403,
        "baby": baby
    }


# 아기 삭제
@router.delete("/", dependencies=[Depends(JWTBearer())])
def delete_baby(baby_id: str,
                parent_id: str = Depends(JWTBearer())) -> DeleteBabyOutput:
    
    # 부모 아이디가 없으면 에러
    if parent_id == None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Invalid parent_id")
    # 아기 삭제
    success = babyService.deleteBaby(parent_id, baby_id)

    return {
        "success": 200 if success else 403,
    }


# 아기 정보 가져오기 (확인용 임시 코드)
@router.get("/all")
def get_babies():
    babies = babyService.getBabies()
    return babies
