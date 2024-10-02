from pydantic import BaseModel
from typing import Optional, Dict

from model.friend import Friend


class CreateFriendInput(BaseModel):
    friend: str

class DeleteFriendInput(BaseModel):
    friend: str