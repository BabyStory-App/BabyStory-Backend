from typing import Optional, List
from datetime import datetime

from model.post import *
from schemas.pagination import *


class SettingOverviewOutputData(BaseModel):
    mateCount: int
    friendCount: int
    myStoryCount: int

class SettingOverviewOutputService(BaseModel):
    status: int
    message: str
    data: SettingOverviewOutputData


# 친구인 부모 정보
class FriendsParent(BaseModel):
    parent_id: str
    nickname: str
    photoId: Optional[str]
    description: Optional[str]
    isMate: bool


# 내가 팔로우한 부모 정보
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
    createTime: Optional[datetime]
    pHeart: Optional[int] = 0
    pScript: Optional[int] = 0
    pView: Optional[int] = 0
    pComment: Optional[int] = 0
    hashList: Optional[str] = None
    contentPreview: str
    photo_id: Optional[str] = None


# 내가 본 포스트
class MyViewsPostOutputService(BaseModel):
    paginationInfo: PaginationInfo
    post: list[Post]

class MyViewsPostOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: list[Post]


# 내가 스크랩트한 포스트
class MyScriptsPostOutputService(BaseModel):
    paginationInfo: PaginationInfo
    post: list[Post]

class MyScriptsPostOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: list[Post]


# 내가 좋아요 누른 포스트
class MyLikesPostOutputService(BaseModel):
    paginationInfo: PaginationInfo
    post: list[Post]

class MyLikesPostOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: list[Post]


class MyStoriesPost(BaseModel):
    post_id: int
    title: str
    createTime: Optional[datetime]
    pHeart: Optional[int] = 0
    pScript: Optional[int] = 0
    pView: Optional[int] = 0
    pComment: Optional[int] = 0
    hashList: Optional[str] = None
    contentPreview: str
    photo_id: Optional[str] = None


# 내가 쓴 포스트
class MyStoriesOutputService(BaseModel):
    paginationInfo: PaginationInfo
    post: list[MyStoriesPost]

class MyStoriesOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: list[MyStoriesPost]


class MatesParent(BaseModel):
    parent_id: str
    nickname: str
    photoId: Optional[str] = None
    description: Optional[str] = None


# 내 짝꿍 정보
class MyMatesOutputService(BaseModel):
    paginationInfo: PaginationInfo
    parents: list[MatesParent]


class MyMatesOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    parents: list[MatesParent]
