from fastapi import UploadFile
from typing import List, Optional, Union
from datetime import datetime
from sqlalchemy import func
import os

from model.cry_state import CryState
from constants.path import BABY_CRY_DATASET_DIR
from model.parent import Parent
from model.types.baby import BabyType
from schemas.baby import BabyCreateInput, BabyUpdateInput
from db import get_db_session
from services.cry_predict import cry_predict


class CryService:
    def __init__(self):
        self.model = CryState

    async def predict(self, file: UploadFile, uid: str) -> dict:
        content = await file.read()

        curtime = datetime.now()
        timestamp = curtime.strftime("%Y%m%d-%H%M%S")
        save_filename = f"{uid}_{timestamp}.wav"
        file_path = os.path.join(BABY_CRY_DATASET_DIR, save_filename)
        with open(file_path, 'wb') as f:
            f.write(content)

        # get predictMap
        print(f'response state:')
        predictMap = await cry_predict(content)
        for key in predictMap:
            print(f'{key}: {predictMap[key]}')

        return {
            "time": curtime.strftime("%Y-%m-%d %H:%M:%S"),
            "filename": file.filename,
            'predictMap': predictMap,
            "intensity": 'medium',
            'audioURL': timestamp,
        }

    async def inspect(self, baby_id: str, year: int, month: int):
        db = get_db_session()
        try:
            # get cry_list of baby_id that has been predicted in month
            cry_list = db.query(self.model).filter(
                self.model.babyId == baby_id,
                func.extract('year', CryState.time) == year,
                func.extract('month', CryState.time) == month,
            ).all()
            print(cry_list)
            print(type(cry_list[0]))

        except Exception as e:
            print(e)
            return None
        return ""
