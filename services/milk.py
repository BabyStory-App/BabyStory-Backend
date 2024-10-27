from fastapi import HTTPException, UploadFile
from typing import Optional, List
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from constants.path import *
from datetime import datetime
from sqlalchemy import func
import os

from schemas.milk import *
from model.milk import *
from model.diary import *
from db import get_db_session
from error.exception.customerror import *

class MilkService:

    # 수유일지 생성
    def createMilk(self, parent_id: str, createMilkInput: CreateMilkInput) -> Milk:
        """
        수유일지 생성
        - input
            - parent_id (str): 부모 아이디
            - createMilkInput (CreateMilkInput): 수유일지 생성 정보
        - output
            - milk (Milk): 수유일지 딕셔너리
        """
        
        db = get_db_session()

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == createMilkInput.diary_id,
            DiaryTable.parent_id == parent_id).first()
        
        if diary is None:
            raise CustomException("Diary does not exist")
        
        milk = MilkTable(
            diary_id=createMilkInput.diary_id,
            baby_id=createMilkInput.baby_id,
            milk=createMilkInput.milk,
            amount=createMilkInput.amount,
            mtime=createMilkInput.mtime
        )

        try:
            db.add(milk)
            db.commit()
            db.refresh(milk)
        except Exception as e:
            db.rollback()
            raise CustomException("Failed to create milk")
        
        return milk
    

    # 다이어리에 대한 전체 수유일지 조회
    def getAllMilk(self, parent_id: str, getMilkInput: GetMilkInput) -> List[Milk]:
        """
        다이어리에 대한 전체 수유일지 조회
        - input
            - parent_id (str): 부모 아이디
            - getMilkInput (GetMilkInput): 수유일지 조회 정보
        - output
            - milks (List[Milk]): 수유일지 리스트
        """
        
        db = get_db_session()

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == getMilkInput.diary_id,
            DiaryTable.parent_id == parent_id).first()
        
        if diary is None:
            raise CustomException("Diary does not exist")
        
        milks = db.query(MilkTable).filter(
            MilkTable.diary_id == getMilkInput.diary_id).all()
        
        return milks
    

    # 해당 날짜의 모든 수유일지 조회
    def getMilk(self, parent_id: str,
                diary_id: str, create_time: datetime) -> List[Milk]:
        """
        해당 날짜의 수유일지 조회
        - input
            - parent_id (str): 부모 아이디
            - getMilkInput (GetMilkInput): 수유일지 조회 정보
        - output
            - milks (List[Milk]): 수유일지 리스트
        """
        
        db = get_db_session()

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == diary_id,
            DiaryTable.parent_id == parent_id).first()
        
        if diary is None:
            raise CustomException("Diary does not exist")
        
        milks = db.query(MilkTable).filter(
            MilkTable.diary_id == diary_id,
            func.date(MilkTable.mtime) == create_time).all()
        
        return milks
    

    # 수유일지 수정
    def updateMilk(parent_id: str,
                   UpdateMilkInput: UpdateMilkInput) -> Milk:
        """
        수유일지 수정
        - input
            - parent_id (str): 부모 아이디
            - milk_id (int): 수유일지 아이디
        - output
            - milk (Milk): 수유일지 딕셔너리
        """
        
        db = get_db_session()

        diary = db.execute(text(
            f"SELECT * FROM diary \
            WHERE diary_id = (SELECT diary_id FROM milk WHERE milk_id = {UpdateMilkInput.milk_id}) \
            AND parent_id = '{parent_id}'")).fetchone()
        
        if diary is None:
            raise CustomException("Diary does not exist")
        
        milk = db.query(MilkTable).filter(
            MilkTable.milk_id == UpdateMilkInput.milk_id).first()
        
        if milk is None:
            raise CustomException("Milk does not exist")
        
        milk.milk = milk.milk
        milk.amount = milk.amount
        milk.mtime = milk.mtime

        try:
            db.commit()
            db.refresh(milk)
        except Exception as e:
            db.rollback()
            raise CustomException("Failed to update milk")
        
        return milk
    

    # 수유일지 삭제
    def deleteMilk(parent_id: str, milk_id: int) -> bool:
        """
        수유일지 삭제
        - input
            - parent_id (str): 부모 아이디
            - milk_id (int): 수유일지 아이디
        - output
            - bool: True
        """
        
        db = get_db_session()

        diary = db.execute(text(
            f"SELECT * FROM diary \
            WHERE diary_id = (SELECT diary_id FROM milk WHERE milk_id = {milk_id}) \
            AND parent_id = '{parent_id}'")).fetchone()
        
        if diary is None:
            raise CustomException("Diary does not exist")
        
        milk = db.query(MilkTable).filter(
            MilkTable.milk_id == milk_id).first()
        
        if milk is None:
            raise CustomException("Milk does not exist")
        
        try:
            db.delete(milk)
            db.commit()
        except Exception as e:
            db.rollback()
            raise CustomException("Failed to delete milk")
        
        return True