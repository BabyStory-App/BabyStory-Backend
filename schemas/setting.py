from typing import Optional, List
from datetime import datetime

from model.post import *
from schemas.pagination import *

class SettingOverviewOutputData(BaseModel):
    mateCount: int
    friendCount: int
    myStoryCount: int

class SettingOverviewOutputService(BaseModel):
    data: SettingOverviewOutputData

class FriendsParent(BaseModel):
    parent_id: str
    nickname: str
    photoId: Optional[str]
    description: Optional[str]
    isMate: bool

class MyFriendsOutputService(BaseModel):
    paginationInfo: PaginationInfo
    parents: List[FriendsParent]

class MyFriendsOutputService(BaseModel):
    paginationInfo: PaginationInfo
    parents: List[FriendsParent]

class Post(BaseModel):
    post_id: int
    title: str
    createTime: datetime
    heart: int
    comment: int
    script: int
    view: int
    hashList: str
    contentPreview: str
    photo_id: Optional[str]

class MyViewsPostOutputService(BaseModel):
    paginationInfo: PaginationInfo
    post: list[Post]

class MyScriptsPostOutputService(BaseModel):
    paginationInfo: PaginationInfo
    post: list[Post]

class MyLikesPostOutputService(BaseModel):
    paginationInfo: PaginationInfo
    post: list[Post]

class MyStoriesOutputService(BaseModel):
    paginationInfo: PaginationInfo
    post: list[Post]

class MatesParent(BaseModel):
    parent_id: str
    nickname: str
    photoId: Optional[str]
    description: Optional[str]

class MyMatesOutputService(BaseModel):
    paginationInfo: PaginationInfo
    parents: list[MatesParent]