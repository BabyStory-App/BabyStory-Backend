from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.post import *
from model.parent import *

class CreateSearchInput(BaseModel):
    search: str
    size: int
    page: int

class CreateSearchOutput(BaseModel):
    title: str
    photo_id: str
    author_name: str
    heart: int
    comment: int
    desc: str

class CreateSearchOutputListOutput(BaseModel):
    banners: List[CreateSearchOutput]

class CreateSearchRecommendInput(BaseModel):
    type: str
    size: int
    page: int
    

