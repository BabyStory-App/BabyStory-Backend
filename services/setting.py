from fastapi import HTTPException, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional, List
from sqlalchemy.orm import joinedload
from constants.path import *
import os
import shutil
from uuid import uuid4
from sqlalchemy import text
from sqlalchemy.orm import aliased
import ast

from schemas.setting import *
from schemas.setting import *
from db import get_db_session
from error.exception.customerror import *

from model.friend import FriendTable
from model.parent import ParentTable
from model.post import PostTable
from model.pview import PViewTable
from model.pscript import PScriptTable
from model.pheart import PHeartTable

class SettingService:
    
    # 짝꿍, 친구들, 이야기 수 가져오기
    def getOverview(self, parent_id: str) -> Optional[SettingOverviewOutputData]:
        """
        짝꿍, 친구들, 이야기 수 가져오기
        - input
            - parent_id (str): 부모 아이디
        - output
            - SettingOverviewOutputData: 짝꿍, 친구들, 이야기 수
        """
        db = get_db_session()

        # 내가 친구로 등록한 부모 수
        friendCount = db.query(FriendTable).filter(FriendTable.parent_id == parent_id).count()

        # 짝꿍 수
        mateCount = int(db.execute(text(
            f"select count(0) from friend p inner join friend f \
            on p.parent_id = f.friend where p.parent_id = \"{parent_id}\"")).fetchall()[0][0])

        # 이야기 수
        myStoryCount = db.query(PostTable).filter(
            PostTable.parent_id == parent_id, 
            PostTable.deleteTime == None).count()
        
        return {'friendCount': friendCount, 'mateCount': mateCount, 'myStoryCount': myStoryCount}
    


    # 내가 친구로 등록한 부모 불러오기
    def getMyFriends(self, page: int, parent_id: str) -> Optional[MyFriendsOutput]:
        """
        친구들 불러오기
        - input
            - page (int): 페이지
            - parent_id (str): 부모 아이디
        - output
            - MyFriendsOutput: 친구들
        """
        db = get_db_session()

        # 페이징
        if page != -1 and page < 0:
            raise CustomException("page must be -1 or greater than 0")
        take = 10

        total = db.query(FriendTable).filter(FriendTable.parent_id == parent_id).count()
        
        paginationInfo = {'page': page, 'take': take, 'total': total}

        # 내가 친구로 등록한 부모
        myFriends = db.execute(text(
            f"select p.* from friend f inner join parent p on p.parent_id = f.friend \
                where f.parent_id = :parent_id LIMIT :limit OFFSET :offset"),
                {"parent_id": parent_id, "limit": ( page + 1 ) * take, "offset": page * 10}).fetchall()
        
        # 짝꿍
        mate = db.execute(text(
            f"select f.parent_id from friend p inner join friend f \
            on f.parent_id = p.friend where p.parent_id = \"{parent_id}\"")).fetchall()

        ismate = []
        for i in mate:
            ismate.append(i[0])

        # 친구들 데이터
        parents = []
        for i in myFriends:
            parents.append({
                'parent_id': i[0],
                'nickname': i[4],
                'photoId': i[8],
                'description': i[9],
                'isMate': True if i[0] in ismate else False
            })

        return [paginationInfo, parents]
    


    # 유저가 조회한 post
    def getMyViews(self, page: int, parent_id: str) -> Optional[MyViewsPostOutput]:
        """
        유저가 조회한 post
        - input
            - page (int): 페이지
            - parent_id (str): 부모 아이디
        - output
            - MyViewsPostOutput: 유저가 조회한 post
        """
        db = get_db_session()

        # 페이징
        if page != -1 and page < 0:
            raise CustomException("page must be -1 or greater than 0")
        take = 10

        total = str(db.execute(text(
        f"select count(0) from post p inner join pview v \
            on p.post_id = v.post_id where v.parent_id = \"{parent_id}\"")).fetchall()[0][0])

        paginationInfo = {'page': page, 'take': take, 'total': total}

        myViews = db.execute(text(
        f"select p.* from post p inner join pview v on p.post_id = v.post_id \
            where v.parent_id = :parent_id LIMIT :limit OFFSET :offset"),
        {"parent_id": parent_id, "limit": ( page + 1 ) * take, "offset": page * 10}).fetchall()
        
        if not myViews:
            return []

        # 유저가 조회한 post 데이터
        posts = []
        for i in myViews:
            posts.append({
                'post_id': i[0],
                'title': i[3],
                'createTime': i[4],
                'heart': i[7],
                'script': i[8],
                'view': i[9],
                'comment': i[10],
                'hashList': i[11],
                'contentPreview': str(i[0]) + '_1',
                'photo_id': str(i[0])
            })

        return [paginationInfo, posts]
    


    # 유저가 script한 post
    def getScripts(self, page: int, parent_id: str) -> Optional[MyViewsPostOutput]:
        """
        유저가 script한 post
        - input
            - page (int): 페이지
            - parent_id (str): 부모 아이디
        - output
            - MyViewsPostOutput: 유저가 script한 post
        """
        db = get_db_session()

        # 페이징
        if page != -1 and page < 0:
            raise CustomException("page must be -1 or greater than 0")
        take = 10

        total = str(db.execute(text(
        f"select count(0) from post p inner join pscript s \
            on p.post_id = s.post_id where s.parent_id = \"{parent_id}\"")).fetchall()[0][0])

        paginationInfo = {'page': page, 'take': take, 'total': total}

        scripts = db.execute(text(
        f"select * from post p inner join pscript s on p.post_id = s.post_id \
            where s.parent_id = :parent_id LIMIT :limit OFFSET :offset"),
            {"parent_id": parent_id, "limit": ( page + 1 ) * take, "offset": page * 10}).fetchall()

        if not scripts:
            return []
        
        # 유저가 script한 post 데이터
        posts = []
        for i in scripts:
            posts.append({
                'post_id': i[0],
                'title': i[3],
                'createTime': i[4],
                'heart': i[7],
                'script': i[8],
                'view': i[9],
                'comment': i[10],
                'hashList': i[11],
                'contentPreview': str(i[0]) + '_1',
                'photo_id': str(i[0])
            })

        return [paginationInfo, posts]
    


    # 유저가 좋아요한 post
    def getLikes(self, page: int, parent_id: str) -> Optional[MyViewsPostOutput]:
        """
        유저가 좋아요한 post
        - input
            - page (int): 페이지
            - parent_id (str): 부모 아이디
        - output
            - MyViewsPostOutput: 유저가 좋아요한 post
        """
        db = get_db_session()

        # 페이징
        if page != -1 and page < 0:
            raise CustomException("page must be -1 or greater than 0")
        take = 10

        total = db.query(FriendTable).filter(PHeartTable.parent_id == parent_id, 
                                             PostTable.post_id == PHeartTable.post_id).count()
        paginationInfo = {'page': page, 'take': take, 'total': total}

        likes = db.execute(text(
        f"select * from post p inner join pheart h on p.post_id = h.post_id \
            where h.parent_id = :parent_id LIMIT :limit OFFSET :offset"),
            {"parent_id": parent_id, "limit": ( page + 1 ) * take, "offset": page * 10}).fetchall() 

        # 유저가 script한 post 데이터
        posts = []
        for i in likes:
            posts.append({
                'post_id': i[0],
                'title': i[3],
                'createTime': i[4],
                'heart': i[7],
                'script': i[8],
                'view': i[9],
                'comment': i[10],
                'hashList': i[11],
                'contentPreview': str(i[0]) + '_1',
                'photo_id': str(i[0])
            })

        return [paginationInfo, posts]
    


    # 유저 post
    def getMyStories(self, page: int, parent_id: str) -> Optional[MyStoriesOutput]:
        """
        유저 post
        - input
            - page (int): 페이지
            - parent_id (str): 부모 아이디
        - output
            - MyStoriesOutput: 유저 post
        """
        db = get_db_session()

        # 유저 post
        myStories = db.query(PostTable).filter(PostTable.parent_id == parent_id).all()

        # 페이징
        if page != -1 and page < 0:
            raise CustomException("page must be -1 or greater than 0")
        take = 10
        myStories = db.query(PostTable).filter(PostTable.parent_id == parent_id).limit(take).offset(page).all()
        total = db.query(FriendTable).filter(PostTable.parent_id == parent_id ).count()
        paginationInfo = {'page': page, 'take': take, 'total': total}


        # post 사진 가져오기
        

        # 유저 post 데이터
        post = []
        for myStory in myStories:
            posts = {
                'post_id': myStory.post_id,
                'title': PostTable.title,
                'createTime': PostTable.createTime,
                'heart': PostTable.pHeart,
                'comment': PostTable.pComment,
                'script': PostTable.pScript,
                'view': PostTable.pView,
                'hashList': PostTable.hashList,
                'contentPreview': myStory.post_id + '_1',
                'photo_id': myStory.post_id
            }
            post.append(posts)

        return {'paginationInfo': paginationInfo, 'post': post}
    


    # 짝꿍 불러오기
    def getMyMates(self, page: int, parent_id: str) -> Optional[MyMatesOutput]:
        """
        짝꿍 불러오기
        - input
            - page (int): 페이지
            - parent_id (str): 부모 아이디
        - output
            - MyMatesOutput: 짝꿍
        """
        db = get_db_session()

        # 페이징
        if page != -1 and page < 0:
            raise CustomException("page must be -1 or greater than 0")
        take = 10
        # 짝꿍
        # FriendTable을 두 개의 별칭으로 참조
        FriendAlias1 = aliased(FriendTable)
        FriendAlias2 = aliased(FriendTable)

        # 주어진 parent_id의 모든 친구를 찾는 서브쿼리
        subquery = db.query(FriendAlias1.friend).filter(FriendAlias1.parent_id == parent_id).subquery()

        # 상호 친구 관계의 수를 구하는 쿼리
        myMates = db.query(FriendAlias2).filter(
            FriendAlias2.parent_id_(subquery),
            FriendAlias2.friend == parent_id
        ).limit(take).offset(page).all()

        total = db.query(FriendAlias2).filter(
            FriendAlias2.parent_id_(subquery),
            FriendAlias2.friend == parent_id
        ).count()
        paginationInfo = {'page': page, 'take': take, 'total': total}

        # 짝꿍 데이터
        parents = []
        for myMate in myMates:
            parent = {
                'parent_id': myMate.friend,
                'nickname': ParentTable.nickname,
                'photoId': ParentTable.photoId,
                'description': ParentTable.description,
            }
            parents.append(parent)

        return {'paginationInfo': paginationInfo, 'parents': parents}