from fastapi import HTTPException
from typing import Optional, List
from sqlalchemy.orm import joinedload

from model.baby import Baby
from model.pbconnect import *

from schemas.baby import *

from db import get_db_session


class BabyService:

    # 아기 생성
    def createBaby(self, 
                    createBabyInput: CreateBabyInput) ->Baby:
        db = get_db_session()
        try:
            baby = BabyTable(
                baby_id=createBabyInput.baby_id,
                name=createBabyInput.name,
                gender=createBabyInput.gender,
                birthDate=createBabyInput.birthDate,
                bloodType=createBabyInput.bloodType,
                photoId=createBabyInput.photoId if createBabyInput.photoId else None
            )

            db.add(baby)
            db.commit()
            db.refresh(baby)

            return baby
        
        except Exception as e:
            db.rollback()
            print(e)
            raise Exception("Failed to create baby")
        
    # 아기-부모 관계 생성
    def createPbconnect(self, parent_id: str, baby_id: str) -> Optional[PBConnect]:
        db = get_db_session()
        try:
            pbconnect = PBConnectTable(
                parent_id=parent_id,
                baby_id=baby_id
            )

            db.add(pbconnect)
            db.commit()
            db.refresh(pbconnect)

            return pbconnect

        except Exception as e:
            db.rollback()
            print(e)
            raise Exception("Failed to create pbconnect")

    # 아기 정보 가져오기
    def getBaby(self, parent_id: str) -> List[Baby]:
        db = get_db_session()
        try:
            # 부모 아이디로 아기-부모 연결 정보 가져오기
            has = db.query(PBConnectTable).filter(PBConnectTable.parent_id == parent_id).all()

            # 부모 아이디에 연결된 모든 아기의 아이디를 가져옴
            baby_ids = [i.baby_id for i in has]

            # has에 해당하는 아기정보와 일치하는 아기정보를 가져옴
            baby = db.query(BabyTable).filter(BabyTable.baby_id.in_(baby_ids)).all()
            
            if baby is None:
                return None

            return baby

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to get baby")
            

    # 아기 정보 가져오기 (확인용 임시 코드)
    def getBabies(self):
        db = get_db_session()
        babies = db.query(BabyTable).all()
        return babies

    # 아기 정보 수정
    def updateBaby(self, updateBabyInput: UpdateBabyInput, parent_id: str) -> Optional[Baby]:
        db = get_db_session()

        try:
            # 다른 사람의 아기를 수정하는 것을 방지하기 위해 부모의 아기인지 확인해야함
            pbconnect = db.query(PBConnectTable).filter(
                PBConnectTable.parent_id == parent_id,
                PBConnectTable.baby_id == updateBabyInput.baby_id).first()
            if pbconnect is None:
                return None
            
            baby = db.query(BabyTable).filter(
                BabyTable.baby_id == updateBabyInput.baby_id).first()
            if baby is None:
                return None
            
            # 아기 정보 수정
            for key in ['name', 'gender', 'birthDate', 'bloodType', 'photoId']:
                setattr(baby, key, getattr(updateBabyInput, key))

            db.add(baby)
            db.commit()
            db.refresh(baby)

            return baby
        
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to update baby")

    # 아기 삭제
    def deleteBaby(self, baby_id: str,
                    parent_id: str) -> bool:
        db = get_db_session()
        try:
            # 다른 사람의 아기를 삭제하는 것을 방지하기 위해 부모의 아기인지 확인해야함
            pbconnect = db.query(PBConnectTable).filter(
                PBConnectTable.parent_id == parent_id,
                PBConnectTable.baby_id == baby_id).first()
            if pbconnect is None:
                return False

            # 아기 삭제
            baby = db.query(BabyTable).filter(
                BabyTable.baby_id == baby_id).first()
            if baby == None:
                return False

            db.delete(baby)
            db.commit()

            return True

        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to delete baby")
