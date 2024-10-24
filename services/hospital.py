from fastapi import HTTPException, UploadFile
from typing import Optional, List
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from constants.path import *
from sqlalchemy.exc import SQLAlchemyError

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
            raise HTTPException("Failed to create hospital")

        return hospital

    # 다이어리에 대한 전체 산모수첩 조회

    def getAllHospital(self, parent_id: str,
                       getHospitalInput: GetHospitalInput) -> List[Hospital]:
        """
        다이어리에 대한 전체 산모수첩 조회
        - input
            - getHospitalInput (GetHospitalInput): 다이어리에 대한 전체 산모수첩 조회 정보
        - output
            - hospitals (List[GetHospitalOutput]): 산모수첩 딕셔너리 리스트
        """

        db = get_db_session()

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == getHospitalInput.diary_id,
            DiaryTable.parent_id == parent_id).first()

        if diary is None:
            raise CustomException("Diary does not exist")

        hospitals = db.query(HospitalTable).filter(
            HospitalTable.diary_id == getHospitalInput.diary_id,
            func.date(HospitalTable.createTime) >= getHospitalInput.start_time,
            func.date(HospitalTable.createTime) <= getHospitalInput.end_time).all()

        if hospitals is None:
            raise HTTPException("Hospital does not exist")

        return hospitals

    # 하나의 산모수첩 조회

    def getHospital(self, parent_id: str, hospital_id: int) -> Hospital:
        """
        하나의 산모수첩 조회
        - input
            - parent_id (str): 부모 아이디
            - hospital_id (int): 산모수첩 아이디
        - output
            - hospital (Hospital): 산모수첩 딕셔너리
        """

        db = get_db_session()

        print("hospital_id", hospital_id)
        print("parent_id", parent_id)

        diary = db.execute(text(
            f"""SELECT * FROM diary
            WHERE diary_id=(SELECT diary_id FROM hospital WHERE hospital_id={hospital_id})
            AND parent_id='{parent_id}'""")).fetchone()

        if diary is None:
            raise CustomException("Diary does not exist")

        hospital = db.query(HospitalTable).filter(
            HospitalTable.hospital_id == hospital_id).first()

        if hospital is None:
            raise HTTPException("Hospital does not exist")

        return hospital

    # 산모수첩 수정

    def updateHospital(self, parent_id: str,
                       updateHospitalInput: UpdateHospitalInput) -> Hospital:

        db = get_db_session()

        diary = db.execute(text(
            f"""SELECT * FROM diary
            WHERE diary_id=(SELECT diary_id FROM hospital WHERE hospital_id={updateHospitalInput.hospital_id})
            AND parent_id='{parent_id}'""")).fetchone()

        if diary is None:
            raise CustomException("Diary does not exist")

        hospital = db.query(HospitalTable).filter(
            HospitalTable.hospital_id == updateHospitalInput.hospital_id).first()

        if hospital is None:
            raise CustomException("Hospital does not exist")

        for key in ['parent_kg', 'bpressure', 'baby_kg', 'baby_cm', 'special', 'next_day']:
            hospital.__setattr__(
                key, updateHospitalInput.__getattribute__(key))

        try:
            db.add(hospital)
            db.commit()
            db.refresh(hospital)
        except Exception as e:
            db.rollback()
            raise HTTPException("Failed to update hospital")

        return hospital

    # 산모수첩 삭제


def deleteHospital(parent_id: str, hospital_id: int) -> bool:
    """
    산모수첩 삭제
    - input
        - parent_id (str): 부모 아이디
        - hospital_id (int): 산모수첩 아이디
    - output
        - bool: True
    """

    db = get_db_session()

    diary = db.execute(
        text("""
            SELECT * FROM diary
            WHERE diary_id = (
                SELECT diary_id FROM hospital WHERE hospital_id = :hospital_id
            )
            AND parent_id = :parent_id
        """),
        {"hospital_id": hospital_id, "parent_id": parent_id}
    ).fetchone()

    if diary is None:
        raise CustomException("Diary does not exist")

    hospital = db.query(HospitalTable).filter(
        HospitalTable.hospital_id == hospital_id
    ).first()

    if hospital is None:
        raise CustomException("Hospital does not exist")

    try:
        db.delete(hospital)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to delete hospital")

    return True
