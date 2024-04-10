from typing import List, Optional, Union
from fastapi import UploadFile
import shutil
import os
from uuid import uuid4

from db import get_db_session
from constants.path import PROFILE_IMAGE_DIR
from model.baby import *
from schemas.baby import *


class BabyService:
    def __init__(self):
        self.baby_model = BabyTable

    # 아기 생성
    def create_baby(self, parent_id: str,
                    create_baby_input: create_baby_input) -> BabyTable:
        db = get_db_session()
        try:
            baby = BabyTable(
                baby_id=create_baby_input.baby_id,
                name=create_baby_input.name,
                gender=create_baby_input.gender,
                birthDate=create_baby_input.birthDate,
                bloodType=create_baby_input.bloodType,
                photoId=create_baby_input.photoId if create_baby_input.photoId else None
            )
            db.add(baby)
            db.commit()
            db.refresh(baby)

            # 아기-부모 관계 테이블에 추가

            return baby
        except Exception as e:
            db.rollback()
            print(e)
            raise Exception("Failed to create baby")

    def get_babies(self):
        pass

    # 아기 정보 수정
    def update_baby(self, baby_id: str, update_baby_input: update_baby_input) -> Optional[BabyTable]:
        db = get_db_session()
        try:
            baby = db.query(BabyTable).filter(
                BabyTable.baby_id == baby_id).first()
            if baby is None:
                return None

            for key in ['name', 'gender', 'birthDate', 'bloodType', 'photoId']:
                setattr(baby, key, update_baby_input[key])
            # setattr(baby, 'name', update_baby_input['name'])
            # setattr(baby, 'gender', update_baby_input['gender'])
            # setattr(baby, 'birthDate', update_baby_input['birthDate'])
            # setattr(baby, 'bloodType', update_baby_input['bloodType'])
            # setattr(baby, 'photoId', update_baby_input['photoId'])

            db.add(baby)
            db.commit()
            db.refresh(baby)

            return baby
        except Exception as e:
            db.rollback()
            raise e

    # 아기 삭제
    def delete_baby(self, parent_id: str,
                    baby_id: str) -> Optional[Baby]:
        db = get_db_session()
        try:
            baby = db.query(BabyTable).filter(
                BabyTable.baby_id == baby_id).first()
            if baby == None:
                return None

            db.delete(baby)
            db.commit()

            return True

        except Exception as e:
            db.rollback()
            return False
