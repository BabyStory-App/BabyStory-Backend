from fastapi import HTTPException, UploadFile
from typing import Optional, List
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from constants.path import *
from datetime import datetime
from sqlalchemy import func
import os
import shutil

from schemas.dday import *
from model.dday import *
# from model.pbconnect import *
# from model.diary import *
from db import get_db_session
from error.exception.customerror import *

class DdayService:

    # DDay 생성
    def createDDay(self, parent_id: str, createDDayInput: CreateDDayInput) -> Dday:
        """
        DDay 생성
        - input
            - parent_id (str): 부모 아이디
            - createDDayInput (CreateDDayInput): DDay 생성 정보
        - output
            - dday (Dday): DDay 딕셔너리
        """
        
        db = get_db_session()

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == createDDayInput.diary_id,
            DiaryTable.parent_id == parent_id).first()
        
        if diary is None:
            raise CustomException("Diary does not exist")
        
        ddays = db.query(DdayTable).filter(
            DdayTable.diary_id == createDDayInput.diary_id,
            func.date(DdayTable.createTime) == datetime.now().date()).first()

        
        if ddays is not None:
            raise CustomException("DDay already exists")
        
        dday = DdayTable(
            diary_id=createDDayInput.diary_id,
            parent_id=parent_id,
            title=createDDayInput.title,
            createTime=datetime.now(),
            modifyTime=None
        )

        try:
            db.add(dday)
            db.commit()
            db.refresh(dday)
        except Exception as e:
            db.rollback()
            raise HTTPException(e)

        # content 파일의 tempddayId를 dday_id로 변경
        content = createDDayInput.content.replace(
            "![[tempddayId", f"![[{dday.dday_id}")
        
        # content를 txt 파일로 저장
        file_path = os.path.join(DIARY_DAY_CONTENT_DIR, str(dday.dday_id) + '.txt')
        with open(file_path, 'w', encoding='UTF-8') as f:
            f.write(content)
        
        return dday
    
    
    # DDay 사진 추가
    def addDDayImage(self, parent_id: str, dday_id: int, fileList: List[UploadFile]) -> UploadImageOutput:
        """
        DDay 사진 추가
        - input
            - parent_id (str): 부모 아이디
            - dday_id (int): DDay 아이디
            - image (UploadFile): 이미지 파일
        - output
            - ddayImage (DdayImage): DDay 이미지 딕셔너리
        """
        
        db = get_db_session()

        dday = db.query(DdayTable).filter(
            DdayTable.dday_id == dday_id,
            DdayTable.parent_id == parent_id).first()

        if dday is None:
            raise CustomException("DDay does not exist")

        # DDay 사진에 대한 디렉토리를 생성합니다.
        os.makedirs(os.path.join(DIARY_DAY_PHOTO_DIR, str(dday.dday_id)), exist_ok=True)

        # 생성된 디렉토리에 사진을 저장합니다.
        for i, file in enumerate(fileList):
            file_type = file.content_type.split('/')[1]
            file_path = os.path.join(DIARY_DAY_PHOTO_DIR, str(
                dday.dday_id), f"{dday.dday_id}_{i + 1}.{file_type}")
            
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(file.file, f)

        return True


    # DDay 가져오기
    def getDDay(self, parent_id: str, diary_id: int, create_time: str) -> getdday:
        """
        DDay 가져오기
        - input
            - parent_id (str): 부모 아이디
            - diary_id (int): 다이어리 아이디
            - create_time (str): 생성 시간
        - output
            - dday (getdday): DDay 딕셔너리
        """
        
        db = get_db_session()

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == diary_id,
            DiaryTable.parent_id == parent_id).first()
        
        if diary is None:
            raise CustomException("Diary does not exist")

        day = db.query(DdayTable).filter(
            DdayTable.diary_id == diary_id,
            DdayTable.parent_id == parent_id,
            func.date(DdayTable.createTime) == create_time).first()
        
        if day is None:
            raise CustomException("DDay does not exist")
        
        
        # hospital = db.query(HospitalTable.hospital_id).filter(
        #     HospitalTable.diary_id == day.diary_id,
        #     func.date(HospitalTable.createTime) == create_time).first()
        
        dday = []
        dday.append({
            "dday_id": day.dday_id,
            "diary_id": day.diary_id,
            "title": day.title,
            "post": day.post,
            "createTime": day.createTime,
            "modifyTime": day.modifyTime,
            "hospital_id": 1
        })
        
        return dday