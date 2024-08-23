from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class PaginationInfo(BaseModel):
    page: int
    take: int
    total: int