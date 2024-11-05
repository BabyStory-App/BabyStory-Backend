from fastapi import HTTPException, UploadFile
from typing import Optional, List
from sqlalchemy import text, desc
from sqlalchemy.orm import joinedload
from constants.path import *
from datetime import datetime
from sqlalchemy import func
import os
import shutil
import re

from schemas.dday import *
from model.dday import *
from model.hospital import *
from model.milk import *
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

        createTime = datetime.strptime(createDDayInput.createTime, "%Y-%m-%d")

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == createDDayInput.diary_id,
            DiaryTable.parent_id == parent_id,
            DiaryTable.deleteTime == None).first()

        if diary is None:
            raise CustomException("Diary does not exist")

        ddays = db.query(DdayTable).filter(
            DdayTable.diary_id == createDDayInput.diary_id,
            func.date(DdayTable.createTime) == createTime,
            DdayTable.deleteTime == None).first()

        if ddays is not None:
            raise CustomException("DDay already exists")

        dday = DdayTable(
            diary_id=createDDayInput.diary_id,
            parent_id=parent_id,
            title=createDDayInput.title,
            createTime=createTime,
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
        file_path = os.path.join(
            DIARY_DAY_CONTENT_DIR, str(dday.dday_id) + '.txt')
        with open(file_path, 'w', encoding='UTF-8') as f:
            f.write(content)

        return dday

    # DDay 사진 추가

    def uploadDDayPhoto(self, parent_id: str, dday_id: int, fileList: List[UploadFile]) -> bool:
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
            DdayTable.parent_id == parent_id,
            DdayTable.deleteTime == None).first()

        if dday is None:
            raise CustomException("DDay does not exist")

        # DDay 사진에 대한 디렉토리를 생성합니다.
        os.makedirs(os.path.join(DIARY_DAY_PHOTO_DIR,
                    str(dday.dday_id)), exist_ok=True)

        # 생성된 디렉토리에 사진을 저장합니다.
        for i, file in enumerate(fileList):
            file_type = file.content_type.split('/')[1]
            file_path = os.path.join(DIARY_DAY_PHOTO_DIR, str(
                dday.dday_id), f"{dday.dday_id}-{i + 1}.{file_type}")

            with open(file_path, 'wb') as f:
                shutil.copyfileobj(file.file, f)

        return True

    # 산모수첩에 대한 전체 DDay 조회

    def getAllDDay(self, parent_id: str, diary_id: int) -> List:
        """
        산모수첩에 대한 전체 DDay 조회
        - input
            - parent_id (str): 부모 아이디
            - diary_id (int): 다이어리 아이디
        - output
            - dday (allday): DDay 딕셔너리
        """

        db = get_db_session()

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == diary_id,
            DiaryTable.parent_id == parent_id,
            DiaryTable.deleteTime == None).first()

        if diary is None:
            raise CustomException("Diary does not exist")

        ddays = db.query(DdayTable).filter(
            DdayTable.diary_id == diary_id,
            DdayTable.parent_id == parent_id,
            DdayTable.deleteTime == None).order_by(desc(DdayTable.createTime)).all()

        if ddays is None:
            return []

        dday = []
        for d in ddays:
            dday.append({
                "dday_id": d.dday_id,
                "title": d.title,
                "createTime": d.createTime
            })
        return dday

    def getOneDDayById(self, parent_id: str, dday_id: int) -> getdday:
        """
        DDay 가져오기
        - input
            - parent_id (str): 부모 아이디
            - dday_id (int): dday 아이디
        - output
            - dday (getdday): DDay 딕셔너리
        """

        db = get_db_session()

        day = db.query(DdayTable).filter(
            DdayTable.dday_id == dday_id,
            DdayTable.parent_id == parent_id,
            DdayTable.deleteTime == None).first()

        if day is None:
            raise CustomException("DDay does not exist")

        content = ''
        content_file_path = os.path.join(DIARY_DAY_CONTENT_DIR,
                                         str(day.dday_id) + '.txt')
        if os.path.exists(content_file_path):
            content = open(content_file_path, 'r', encoding='UTF-8').read()
        match = re.findall(r'!\[\[(.*?)\]\]', content)

        dday = {
            "dday_id": day.dday_id,
            "diary_id": day.diary_id,
            "title": day.title,
            "content": content,
            "photoId": match if match else None,
            "createTime": day.createTime,
            "modifyTime": day.modifyTime,
        }

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == day.diary_id,
            DiaryTable.parent_id == parent_id,
            DiaryTable.deleteTime == None).first()

        # 산모수첩인 경우
        if diary.born == 0:
            hospital = db.query(HospitalTable.hospital_id).filter(
                HospitalTable.diary_id == day.diary_id,
                func.date(HospitalTable.createTime) == day.createTime).first()

            dday['add'] = {"hospital": hospital[0]
                           if hospital is not None else None}

        # 육아수첩인 경우
        else:
            milks = db.query(MilkTable).filter(
                MilkTable.diary_id == day.diary_id,
                func.date(MilkTable.mtime) == day.createTime).all()

            milk = [None] * len(milks)
            for m in range(len(milks)):
                milk[m] = milks[m].milk_id

            dday['add'] = {"milk": milk if milk is not [] else None}

        return dday

    def getOneDDay(self, parent_id: str, diary_id: int, create_time: str) -> getdday:
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
            DiaryTable.parent_id == parent_id,
            DiaryTable.deleteTime == None).first()

        if diary is None:
            raise CustomException("Diary does not exist")

        day = db.query(DdayTable).filter(
            DdayTable.diary_id == diary_id,
            DdayTable.parent_id == parent_id,
            func.date(DdayTable.createTime) == create_time,
            DdayTable.deleteTime == None).first()

        if day is None:
            raise CustomException("DDay does not exist")

        content = ''
        content_file_path = os.path.join(DIARY_DAY_CONTENT_DIR,
                                         str(day.dday_id) + '.txt')
        if os.path.exists(content_file_path):
            content = open(content_file_path, 'r', encoding='UTF-8').read()
        match = re.findall(r'!\[\[(.*?)\]\]', content)

        dday = {
            "dday_id": day.dday_id,
            "diary_id": day.diary_id,
            "title": day.title,
            "content": content,
            "photoId": match if match else None,
            "createTime": day.createTime,
            "modifyTime": day.modifyTime,
        }

        # 산모수첩인 경우
        if diary.born == 0:
            hospital = db.query(HospitalTable.hospital_id).filter(
                HospitalTable.diary_id == day.diary_id,
                func.date(HospitalTable.createTime) == create_time).first()

            dday['add'] = {"hospital": hospital[0]
                           if hospital is not None else None}

        # 육아수첩인 경우
        else:
            milks = db.query(MilkTable).filter(
                MilkTable.diary_id == day.diary_id,
                func.date(MilkTable.mtime) == create_time).all()

            milk = [None] * len(milks)
            for m in range(len(milks)):
                milk[m] = milks[m].milk_id

            dday['add'] = {"milk": milk if milk is not [] else None}

        return dday

    # DDay 수정

    def updateDDay(self, parent_id: str, updateDDayInput: UpdateDDayInput) -> getdday:
        """
        DDay 수정
        - input
            - parent_id (str): 부모 아이디
            - updateDDayInput (UpdateDDayInput): DDay 수정 정보
        - output
            - dday (getdday): DDay 딕셔너리
        """

        db = get_db_session()

        day = db.query(DdayTable).filter(
            DdayTable.dday_id == updateDDayInput.dday_id,
            DdayTable.parent_id == parent_id,
            DdayTable.deleteTime == None).first()

        if day is None:
            raise CustomException("DDay does not exist")

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == day.diary_id,
            DiaryTable.parent_id == parent_id,
            DiaryTable.deleteTime == None).first()

        if diary is None:
            raise CustomException("Diary does not exist")

        if updateDDayInput.title is not None:
            day.title = updateDDayInput.title
        day.modifyTime = datetime.now()

        try:
            db.commit()
            db.refresh(day)
        except Exception as e:
            db.rollback()
            raise e

        file_path = os.path.join(
            DIARY_DAY_CONTENT_DIR, str(day.dday_id) + '.txt')
        if updateDDayInput.content != None:
            with open(file_path, 'w', encoding='UTF-8') as f:
                f.write(updateDDayInput.content)
            content = updateDDayInput.content
        else:
            print(file_path)
            with open(file_path, 'r', encoding='UTF-8') as f:
                content = f.read()
            print(content)

        create_time = day.createTime.strftime("%Y-%m-%d")

        dday = {
            "dday_id": day.dday_id,
            "diary_id": day.diary_id,
            "title": day.title,
            "content": content,
            "createTime": day.createTime,
            "modifyTime": day.modifyTime
        }

        # 산모수첩인 경우
        if diary.born == 0:
            hospital = db.query(HospitalTable.hospital_id).filter(
                HospitalTable.diary_id == day.diary_id,
                func.date(HospitalTable.createTime) == create_time).first()
            dday['add'] = {"hospital": hospital[0]
                           if hospital is not None else None}
        # 육아수첩인 경우
        else:
            milks = db.query(MilkTable).filter(
                MilkTable.diary_id == day.diary_id,
                func.date(MilkTable.mtime) == create_time).all()

            milk = [None] * len(milks)
            for m in range(len(milks)):
                milk[m] = milks[m].milk_id

            dday['add'] = {"milk": milk if milk is not [] else None}

        return dday

    # DDay 사진 수정

    def updateDDayPhoto(self, parent_id: str, dday_id: int, fileList: List[UploadFile]) -> bool:
        """
        DDay 사진 수정
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
            DdayTable.parent_id == parent_id,
            DdayTable.deleteTime == None).first()

        if dday is None:
            raise CustomException("DDay does not exist")

        folder_path = os.path.join(DIARY_DAY_PHOTO_DIR, str(dday_id))
        # DDay 사진 중 마지막 사진의 번호를 가져온다.
        if os.path.isdir(folder_path):
            num = len(os.listdir(folder_path))
        else:
            raise CustomException("DDay photo not found")

        # 생성된 디렉토리에 사진을 저장합니다.
        for i, file in enumerate(fileList):
            file_type = file.content_type.split('/')[1]
            file_path = os.path.join(DIARY_DAY_PHOTO_DIR, str(
                dday.dday_id), f"{dday.dday_id}-{num + 1}.{file_type}")
            num += 1

            with open(file_path, 'wb') as f:
                shutil.copyfileobj(file.file, f)

        return True

    # DDay 삭제

    def deleteDDay(self, parent_id: str, dday_id: int) -> bool:
        """
        DDay 삭제
        - input
            - parent_id (str): 부모 아이디
            - dday_id (int): DDay 아이디
        - output
            - success (bool): 성공 여부
        """

        db = get_db_session()

        dday = db.query(DdayTable).filter(
            DdayTable.dday_id == dday_id,
            DdayTable.parent_id == parent_id,
            DdayTable.deleteTime == None).first()

        if dday is None:
            raise CustomException("DDay does not exist")

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == dday.diary_id,
            DiaryTable.parent_id == parent_id,
            DiaryTable.deleteTime == None).first()

        if diary is None:
            raise CustomException("Diary does not exist")

        dday.deleteTime = datetime.now()

        try:
            db.commit()
            db.refresh(dday)
        except Exception as e:
            db.rollback()
            raise e

        return True
