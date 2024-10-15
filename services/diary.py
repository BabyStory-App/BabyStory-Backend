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
        
        # 생성된 디렉토리에 사진을 저장
        file_type = file.filename.split('.')[-1]
        file_path = os.path.join(DIARY_COVER_PATH, f'{diary_id}.{file_type}')
        
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)

        return True