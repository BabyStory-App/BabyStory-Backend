from fastapi import HTTPException, UploadFile
from typing import Optional, List
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from constants.path import *
import os
import re
import shutil
from uuid import uuid4
from datetime import datetime
import random

from schemas.diary import *
from model.diary import Diary
from model.pbconnect import *
from schemas.diary import *
from db import get_db_session
from error.exception.customerror import *

class DiaryService:

    # 다이어리 생성
    def createDiary(self, parent_id: str,
                    createDiaryInput: CreateDiaryInput,) -> CreateDiaryOutput:
        """
        다이어리 생성
        - input
            - parent_id (str): 부모 아이디
            - createDiaryInput (CreateDiaryInput): 다이어리 생성 정보
        - output
            - diary (Diary): 다이어리 딕셔너리
        """
        
        db = get_db_session()

        # 아기에 대한 산모수첩이 이미 존재하는지 확인
        if createDiaryInput.born == 0:
            pregnancy = db.query(DiaryTable).filter(
            DiaryTable.baby_id == createDiaryInput.baby_id,
            DiaryTable.born == createDiaryInput.born).first()
        
            if pregnancy is not None:
                raise CustomException("Pregnancy Diary already exists")
            
        # born이 산모수첩 또는 육아일기인지 확인
        if createDiaryInput.born not in [0, 1]:
            raise CustomException("Invalid born value")

        diary = DiaryTable(
            parent_id=parent_id,
            baby_id=createDiaryInput.baby_id,
            born=createDiaryInput.born,
            title=createDiaryInput.title,
            createTime=datetime.now(),
            modifyTime=None,
            deleteTime=None
        )

        try:
            db.add(diary)
            db.commit()
            db.refresh(diary)
        except Exception as e:
            db.rollback()
            raise e
        
        return diary
    

    # 다이어리 표지 사진 업로드
    def uploadDiaryCover(self, parent_id: str,
                         file: UploadFile,
                         diary_id: int) -> UploadDiaryCoverOutput:
        """
        다이어리 표지 사진 업로드
        - input
            - parent_id (str): 부모 아이디
            - file (UploadFile): 업로드 파일
        - output
            - success (int): 성공 여부
        """
        db = get_db_session()

        diary = db.query(DiaryTable).filter(
            DiaryTable.parent_id == parent_id,
            DiaryTable.diary_id == diary_id,
            DiaryTable.deleteTime == None).first()
        
        # 다이어리가 없을 경우 CustomException을 발생
        if diary is None:
            raise CustomException("Diary not found")
        
        # 다이어리 표지 사진이 이미 존재할 경우 에러 발생
        with os.scandir(DIARY_COVER_PATH) as entries:
            for entry in entries:
                if entry.name.startswith(str(diary_id) + '.'):
                    raise CustomException("Diary cover image already exists")

        # 생성된 디렉토리에 사진을 저장
        file_type = file.filename.split('.')[-1]
        file_path = os.path.join(DIARY_COVER_PATH, f'{diary_id}.{file_type}')
        
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)

        return True
    
    # 아기의 모든 다이어리 가져오기
    def getAllDiary(self, parent_id: str, baby_id: str) -> GetDiaryOutput:
        """
        아기의 모든 다이어리 가져오기
        - input
            - parent_id (str): 부모 아이디
            - baby_id (str): 아기 아이디
        - output
            - diary (List[Diary]): 다이어리 리스트
        """
        db = get_db_session()

        baby = db.query(BabyTable).filter(
            BabyTable.baby_id == baby_id).first()
        
        # 해당 부모에게 아기가 없는 경우
        if baby is None:
            raise CustomException("Baby not found")
        
        # 해당 부모와 아기가 연결되어있지 않는 경우
        pbconnect = db.query(PBConnectTable).filter(
            PBConnectTable.parent_id == parent_id,
            PBConnectTable.baby_id == baby_id).first()
        
        if pbconnect is None:
            raise CustomException("parent and baby are not connected")
        
        diary = db.query(DiaryTable).filter(
            DiaryTable.parent_id == parent_id,
            DiaryTable.baby_id == baby_id,
            DiaryTable.deleteTime == None).all()
        
        return diary
    
    # 하나의 다이어리 가져오기
    def getDiary(self, parent_id: str, diary_id: int) -> GetDiaryOutput:
        """
        하나의 다이어리 가져오기
        - input
            - parent_id (str): 부모 아이디
            - diary_id (int): 다이어리 아이디
        - output
            - diary (Diary): 다이어리
        """
        db = get_db_session()

        diary = db.query(DiaryTable).filter(
            DiaryTable.parent_id == parent_id,
            DiaryTable.diary_id == diary_id,
            DiaryTable.deleteTime == None).first()
        
        return diary