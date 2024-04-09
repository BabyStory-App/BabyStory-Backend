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
    def create_baby(self, create_baby_input: create_baby_input) -> BabyTable:
        db = get_db_session()
        try:
            baby = BabyTable(
                baby_id = create_baby_input.baby_id,
                name = create_baby_input.name,
                gender = create_baby_input.gender,
                birthDate = create_baby_input.birthDate,
                bloodType = create_baby_input.bloodType,
                photoId = create_baby_input.photoId
            )
            db.add(baby)
            db.commit()
            db.refresh(baby)
            return baby
        except Exception as e:
            db.rollback()
            raise e
        

    def get_baby(self):
        pass

    def get_babies(self):
        pass

    # 아기 정보 수정
    def update_baby(self, baby_id: str, update_baby_input: update_baby_input) -> Optional[BabyTable]:
        db = get_db_session()
        try:
            baby = db.query(BabyTable).filter(BabyTable.baby_id == baby_id).first()
            if baby is None:
                return None
            setattr(baby, 'name', update_baby_input.name)
            setattr(baby, 'gender', update_baby_input.gender)
            setattr(baby, 'birthDate', update_baby_input.birthDate)
            setattr(baby, 'bloodType', update_baby_input.bloodType)
            setattr(baby, 'photoId', update_baby_input.photoId)

            db.add(baby)
            db.commit()
            db.refresh(baby)

            return baby
        except Exception as e:
            db.rollback()
            raise e

    # 아기 삭제
    def delete_baby(self, baby_id: str) -> Optional[Baby]:
        db = get_db_session()
        try:
            baby = db.query(BabyTable).filter(BabyTable.baby_id == baby_id).first()
            if baby == None:
                return None
            
            db.delete(baby)
            db.commit()

            return baby
        
        except Exception as e:
            db.rollback()
            raise e
