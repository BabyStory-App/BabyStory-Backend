from typing import List, Optional, Union
from fastapi import UploadFile
import shutil
import os
from uuid import uuid4

from db import get_db_session
from constants.path import PROFILE_IMAGE_DIR


class 임시모델:
    pass


class BabyService:
    def __init__(self):
        self.model = 임시모델

    def create_baby(self):
        pass

    def get_baby(self):
        pass

    def get_babies(self):
        pass

    def update_baby(self):
        pass

    def delete_baby(self):
        pass
