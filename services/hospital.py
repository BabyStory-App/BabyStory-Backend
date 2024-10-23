from fastapi import HTTPException, UploadFile
from typing import Optional, List
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from constants.path import *
from datetime import datetime
from sqlalchemy import func
import os

from schemas.hospital import *
from model.hospital import *
from model.diary import *
from db import get_db_session
from error.exception.customerror import *

class HospitalService:

    # 산모수첩 생성
    def createHospital(self, parent_id: str, createHospitalInput: CreateHospitalInput) -> Hospital:
        """
        산모수첩 생성
        - input
            - parent_id (str): 부모 아이디
            - createHospitalInput (CreateHospitalInput): 산모수첩 생성 정보
        - output
            - hospital (Hospital): 산모수첩 딕셔너리
        """
        
        db = get_db_session()

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == createHospitalInput.diary_id,
            DiaryTable.parent_id == parent_id).first()
        
        if diary is None:
            raise CustomException("Diary does not exist")
        
        hospitals = db.query(HospitalTable).filter(
            HospitalTable.diary_id == createHospitalInput.diary_id,
            func.date(HospitalTable.createTime) == datetime.now().date()).first()

        if hospitals is not None:
            raise CustomException("Hospital already exists")
        
        hospital = HospitalTable(
            diary_id=createHospitalInput.diary_id,
            parent_id=parent_id,
            baby_id=createHospitalInput.baby_id,
            createTime=datetime.now(),
            parent_kg=createHospitalInput.parent_kg,
            bpressure=createHospitalInput.bpressure,
            baby_kg=createHospitalInput.baby_kg,
            baby_cm=createHospitalInput.baby_cm,
            special=createHospitalInput.special,
            next_day=createHospitalInput.next_day
        )

        try:
            db.add(hospital)
            db.commit()
            db.refresh(hospital)
        except Exception as e:
            db.rollback()
            raise CustomException("Failed to create hospital")
    
        return hospital