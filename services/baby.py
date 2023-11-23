from typing import List, Optional, Union

from model.baby import Baby
from model.parent import Parent
from model.types.baby import BabyType
from schemas.baby import BabyCreateInput, BabyUpdateInput
from db import get_db_session


class BabyService:
    def __init__(self):
        self.model = Baby

    def create_baby(self, parent_id: str, baby_input: BabyCreateInput) -> Union[BabyType, str]:
        db = get_db_session()
        try:
            # check if parent exists
            parent = db.query(Parent).filter(Parent.uid == parent_id).first()
            if parent == None:
                return "Parent not found"

            baby = self.model(
                parentId=parent_id,
                name=baby_input.name,
                gender=baby_input.gender,
                birthDate=baby_input.birthDate,
                bloodType=baby_input.bloodType,
            )
            print(baby)
            db.add(baby)
            db.commit()
            db.refresh(baby)
            return BabyType(**baby.__dict__)

        except Exception as e:
            db.rollback()
            print(e)
            return "Failed to create baby"

    def get_baby(self, parent_id: str, baby_id: str) -> Optional[BabyType]:
        db = get_db_session()
        try:
            # Get Baby from DB with primary key uid
            baby = db.query(self.model).filter(
                self.model.uid == baby_id).first()
            if baby == None:
                return "Baby not found"

            if baby.parentId != parent_id:
                return "Access denied"

            return BabyType(**baby.__dict__)
        except Exception as e:
            return None
