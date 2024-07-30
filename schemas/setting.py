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
    photoId: str
    description: str
    isMate: bool

class MyFriendsOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    parents: FriendsParent

class Post(BaseModel):
    post_id: str
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
    post: Post

class MyScriptsPostOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: Post

class MyLikesPostOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: Post

class MyStoriesOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: Post

class MatesParent(BaseModel):
    parent_id: str
    nickname: str
    photoId: str
    description: str

class MyMatesOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    parents: MatesParent