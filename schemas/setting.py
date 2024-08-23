from typing import Optional, List
from datetime import datetime

from model.post import *
from schemas.pagination import *

class SettingOverviewOutputData(BaseModel):
    mateCount: int
    friendCount: int
    myStoryCount: int

class SettingOverviewOutput(BaseModel):
    status: str
    message: str
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

class MyFriendsOutput(BaseModel):
    status: str
    message: str
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

class MyViewsPostOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: list[Post]

class MyScriptsPostOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: list[Post]

class MyLikesPostOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: list[Post]

class MyStoriesOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: list[Post]

class MatesParent(BaseModel):
    parent_id: str
    nickname: str
    photoId: Optional[str]
    description: Optional[str]

class MyMatesOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    parents: list[MatesParent]