from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer
from services.alert import AlertService
from schemas.alert import *
from typing import Optional

from error.exception.customerror import *
from constants.path import *


router = APIRouter(
    prefix="/alert",
    tags=["alert"],
    responses={404: {"description": "Not found"}},
)

alertService = AlertService()


@router.get("/checked/{alert_ids}", dependencies=[Depends(JWTBearer())])
async def check_alert(alert_ids: str) -> GetCheckAlertOutput:
    '''
    알람을 확인하는 API
    input:
        - alert_ids: 확인할 알람 id
        - parent_id: 부모 id
    output:
        - 알람 확인 결과
        - status: 성공 여부
        - message: 결과 메시지
    '''

    try:
        alert_ids = alert_ids.split(",")
        if alert_ids is None or len(alert_ids) == 0:
            raise CustomException("Invalid alert_ids")

        result = alertService.check_alert(alert_ids)

    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get chat history")

    return {"status": 200 if result else 400,
            "message": "done" if result else "Failed"
            }


@router.get("/", dependencies=[Depends(JWTBearer())])
async def alert(parent_id: str = Depends(JWTBearer())) -> GetAlertOutput:
    '''
    확인하지 않은 알림 리스트 조회
    input:
        - parent_id: 부모 id
    output:
        - 알림 리스트
    '''

    try:
        result = alertService.get_alert_list(parent_id)

    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get alert")

    return {"status": 200,
            "message": "Successfully get new alerts",
            "createTime": datetime.now(),
            "alerts": result
            }


@router.get("/subscribe/{creater_id}", dependencies=[Depends(JWTBearer())])
async def toggle_subscribe(creater_id: str, parent_id: str = Depends(JWTBearer())) -> GetToggleSubscribeOutput:
    '''
    알림 구독 토글 (구독 중이면 해지, 구독 중이 아니면 구독)
    input:
        - creater_id: 구독할 대상 id
        - parent_id: 부모 id
    output:
        - 구독 결과
        - hasSubscribe : 구독 여부
        - message: 결과 메시지
    '''

    try:
        result = alertService.toggle_subscribe(creater_id, parent_id)

    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to toggle subscribe")

    return {"hasSubscribe": result,
            "message": f"Successfully toggle subscribe {creater_id}" if result else f"Successfully toggle unsubscribe {creater_id}"
            }
