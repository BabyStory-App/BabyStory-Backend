from fastapi import HTTPException
from typing import Optional, List, Set
from db import get_db_session
from datetime import datetime

from model.alert import AlertTable
from model.alertsub import AlertSubscribeTable
from model.parent import ParentTable
from schemas.alert import *
from error.exception.customerror import *


class AlertService:
    def check_alert(self, alert_ids: List[str]) -> bool:
        '''
        알람 확인
        input:
            - alert_ids: 확인할 알람 id 리스트 (,로 구분)
        output:
            - boolean: 성공 여부
        '''

        db = get_db_session()

        try:
            for alert_id in alert_ids:
                alert = db.query(AlertTable).filter(
                    AlertTable.alert_id == alert_id).first()

                if alert is None:
                    db.rollback()
                    return False

                alert.hasChecked = True

                db.add(alert)

            db.commit()
            db.refresh(alert)

        except Exception as e:
            db.rollback()
            return False

        return True

    def get_alert_list(self, parent_id: str) -> List[GetAlertListOutput]:
        '''
        확인하지 않은 알림 리스트 조회
        input:
            - parent_id: 부모 id
        output:
            - 알림 리스트
        '''

        db = get_db_session()

        # hadChecked가 False인 알림 리스트 조회
        alerts = db.query(AlertTable).filter(
            AlertTable.parent_id == parent_id, AlertTable.hasChecked == False).all()

        # alerts에서 필요한 정보로 변환
        alerts = [{"alert_id": alert.alert_id,
                   "alert_type": alert.alert_type,
                   "message": alert.message,
                   "creater": {
                       "parent_id": alert.createrId,
                       "nickname": getattr(db.query(ParentTable).filter(
                           ParentTable.parent_id == alert.createrId).first(), 'nickname', None),
                       "photo_id": alert.createrId + ".jpeg"
                   },
                   "action": alert.action
                   } for alert in alerts]

        alerts.reverse()
        return alerts

    def toggle_subscribe(self, creater_id: str, parent_id: str) -> bool:
        '''
        알림 구독 토글 (구독 중이면 해지, 구독 중이 아니면 구독)
        input:
            - creater_id: 구독자 id
            - parent_id: 부모 id
        output:
            - boolean: 성공 여부
        '''

        db = get_db_session()

        try:
            # 이미 구독 중인지 확인
            subscribe = db.query(AlertSubscribeTable).filter(
                AlertSubscribeTable.creater_id == creater_id, AlertSubscribeTable.subscriber_id == parent_id).first()

            if subscribe is None:
                # 구독 중이 아니면 추가
                new_subscribe = AlertSubscribeTable(
                    creater_id=creater_id,
                    subscriber_id=parent_id,
                    createTime=datetime.now())

                db.add(new_subscribe)
                db.commit()
                db.refresh(new_subscribe)

                return True

            else:
                # 구독 중이면 삭제
                db.delete(subscribe)
                db.commit()

                return False

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Failed to toggle subscribe")

    def has_subscribe(self, creater_id: str, parent_id: str) -> bool:
        '''
        알림 구독 여부
        input:
            - creater_id: 구독자 id
            - parent_id: 부모 id
        output:
            - boolean: 성공 여부
        '''

        db = get_db_session()

        try:
            # 이미 구독 중인지 확인
            subscribe = db.query(AlertSubscribeTable).filter(
                AlertSubscribeTable.creater_id == creater_id, AlertSubscribeTable.subscriber_id == parent_id).first()
            return subscribe is not None
        except Exception as e:
            raise HTTPException(
                status_code=400, detail="Failed to toggle subscribe")
