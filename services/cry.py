from fastapi import UploadFile
from typing import List, Optional, Union
from datetime import datetime
from sqlalchemy import func, text
import os
import pandas as pd
import numpy as np
from sqlalchemy.dialects import mysql

from model.cry_state import CryState
from constants.path import BABY_CRY_DATASET_DIR
from model.parent import Parent
from model.types.cry_state import CryStateType
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

    async def inspect(self, baby_id: str, start_date: datetime, end_date: datetime):
        db = get_db_session()
        try:
            # get data with sql query and filter and transform to pandas dataframe
            query = db.query(self.model).filter(
                self.model.babyId == baby_id,
                self.model.time >= start_date,
                self.model.time <= end_date
            )
            sql_query = query.statement.compile(
                dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})

            df = pd.read_sql(sql_query, db.connection())
            print(df)

        except Exception as e:
            print(e)
            return None
        return ""
