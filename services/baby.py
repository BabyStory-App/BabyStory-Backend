from typing import List, Optional, Union
from fastapi import UploadFile
import shutil
import os
from uuid import uuid4

from model.baby import Baby
from model.parent import Parent
from model.types.baby import BabyType
from schemas.baby import BabyCreateInput, BabyUpdateInput
from db import get_db_session
from constants.path import PROFILE_IMAGE_DIR


class BabyService:
    def __init__(self):
        self.model = Baby

    def create_baby(self, parent_id: str, baby_input: BabyCreateInput, file: UploadFile) -> Union[BabyType, str]:
        db = get_db_session()
        try:
            # check if parent exists
            parent = db.query(Parent).filter(Parent.uid == parent_id).first()
            if parent == None:
                return "Parent not found"

            # save profile image if exists
            file_id = None
            if file != None:
                file_id = str(uuid4())
                file_save_path = os.path.join(
                    PROFILE_IMAGE_DIR, f"{file_id}.jpeg")
                with open(file_save_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

            baby_data = {
                'parentId': parent_id,
                'name': baby_input.name,
                'gender': baby_input.gender,
                'birthDate': baby_input.birthDate,
                'bloodType': baby_input.bloodType,
            }
            if file_id:
                baby_data['photoId'] = file_id

            baby = self.model(**baby_data)
            db.add(baby)
            db.commit()
            db.refresh(baby)
            return BabyType(**baby.__dict__)
            # babyType = BabyType(**baby.__dict__)

            # # rename file from file_save_path to babyType.id
            # if file_id:
            #     os.rename(file_save_path, os.path.join(PROFILE_IMAGE_DIR, f"{babyType.id}.jpeg"))
            # return babyType

        except Exception as e:
            db.rollback()
            print(e)
            return "Failed to create baby"

    def get_baby(self, parent_id: str, baby_id: str) -> Union[BabyType, str]:
        db = get_db_session()
        try:
            # Get Baby from DB with primary key uid
            baby = db.query(self.model).filter(
                self.model.id == baby_id).first()
            if baby == None:
                return "Baby not found"

            if baby.parentId != parent_id:
                return "Access denied"

            return BabyType(**baby.__dict__)
        except Exception as e:
            print(e)
            return None

    def get_babies(self, parent_id: str) -> Union[List[BabyType], str]:
        db = get_db_session()
        try:
            babies = db.query(self.model).filter(
                self.model.parentId == parent_id).all()
            if babies == None:
                return "Failed to get babies"

            return [BabyType(**baby.__dict__) for baby in babies]
        except Exception as e:
            return "Failed to get babies"

    def update_baby(self, parent_id: str, baby_input: BabyUpdateInput) -> Union[BabyType, str]:
        db = get_db_session()
        try:
            # check if parent exists
            parent = db.query(Parent).filter(Parent.uid == parent_id).first()
            if parent == None:
                return "Parent not found"

            # check if baby exists
            baby = db.query(self.model).filter(
                self.model.id == str(baby_input.id)).first()

            if baby == None:
                return "Baby not found"

            if baby.parentId != parent_id:
                return "Access denied"

            if baby_input.name != None and baby.name != baby_input.name:
                baby.name = baby_input.name
            if baby_input.gender != None and baby.gender != baby_input.gender:
                baby.gender = baby_input.gender
            if baby_input.birthDate != None and baby.birthDate != baby_input.birthDate:
                baby.birthDate = baby_input.birthDate
            if baby_input.bloodType != None and baby.bloodType != baby_input.bloodType:
                baby.bloodType = baby_input.bloodType
            if baby_input.photoId != None and baby.photoId != baby_input.photoId:
                baby.photoId = baby_input.photoId

            db.commit()
            db.refresh(baby)
            return BabyType(**baby.__dict__)

        except Exception as e:
            db.rollback()
            print(e)
            return "Failed to update baby"

    def delete_baby(self, parent_id: str, baby_id: str) -> Union[bool, str]:
        db = get_db_session()
        try:
            # check if parent exists
            parent = db.query(Parent).filter(Parent.uid == parent_id).first()
            if parent == None:
                return "Parent not found"

            # check if baby exists
            baby = db.query(self.model).filter(
                self.model.id == baby_id).first()

            if baby == None:
                return "Baby not found"

            if baby.parentId != parent_id:
                return "Access denied"

            db.delete(baby)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(e)
            return "Failed to delete baby"
