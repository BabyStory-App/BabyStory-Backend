from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.post import *
from model.parent import *


class CreatePostMainBannerOutput(BaseModel):
    post_id: int
    photo_id: str
    title: str
    author_name: str
    desc: str


class CreatePostMainBannerListOutput(BaseModel):
    banners: List[CreatePostMainBannerOutput]


class CreatePostMainInput(BaseModel):
    parent_id: str
    size: int = -1
    page: int = -1


class CreatePostMainFriendOutput(BaseModel):
    post_id: int
    photo_id: str
    title: str
    author_photo: str
    author_name: str
    hasHeart: bool


class CreatePostMainFriendListOutput(BaseModel):
    banners: List[CreatePostMainFriendOutput]


class CreatePostMainFriendSearchOutput(BaseModel):
    post_id: int
    photo_id: str
    title: str
    pHeart: int
    comment: int
    author_name: str
    desc: str


class CreatePostMainFriendSearchListOutput(BaseModel):
    banners: List[CreatePostMainFriendSearchOutput]


class GetNeighborOutput(BaseModel):
    parent_id: str
    photo_id: str
    name: str
    region: str
    desc: str


class GetNeighborOutputListOutput(BaseModel):
    banners: List[GetNeighborOutput]


class CreatePostMainNeighborOutput(BaseModel):
    post_id: int
    photo_id: str
    title: str
    heart: int
    comment: int
    createTime: datetime
    desc: str


class CreatePostMainNeighborListOutput(BaseModel):
    banners: List[CreatePostMainNeighborOutput]


class CreatePostMainHighViewOutput(BaseModel):
    post_id: int
    photo_id: str
    title: str
    author_name: str
    desc: str


class CreatePostMainHighViewListOutput(BaseModel):
    banners: List[CreatePostMainHighViewOutput]


class CreatePostMainHashtagOutput(BaseModel):
    post_id: int
    photo_id: str
    title: str
    author_name: str
    desc: str
    hash: str


class CreatePostMainHashtagListOutput(BaseModel):
    banners: List[CreatePostMainHashtagOutput]
