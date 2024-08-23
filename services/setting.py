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
            ON p.parent_id = f.friend AND p.friend = f.parent_id \
            where p.parent_id = \"{parent_id}\"")).fetchall()[0][0])

        # 이야기 수
        myStoryCount = db.query(PostTable).filter(
            PostTable.parent_id == parent_id, 
            PostTable.deleteTime == None).count()
        
        return {'friendCount': friendCount, 'mateCount': mateCount, 'myStoryCount': myStoryCount}
    


    # 내가 친구로 등록한 부모 불러오기
    def getMyFriends(self, page: int, parent_id: str) -> Optional[MyFriendsOutputService]:
        """
        친구들 불러오기
        - input
            - page (int): 페이지
            - parent_id (str): 부모 아이디
        - output
            - MyFriendsOutputService: 내가 친구로 등록한 부모와 페이지 정보.
        """
        db = get_db_session()

        # 페이징
        if page != -1 and page < 0:
            raise CustomException("page must be -1 or greater than 0")
        take = 10

        total = db.query(FriendTable).filter(FriendTable.parent_id == parent_id).count()

        # 내가 친구로 등록한 부모 찾기
        myFriends = db.execute(text(
            f"select p.* from friend f inner join parent p on p.parent_id = f.friend \
                where f.parent_id = :parent_id LIMIT :limit OFFSET :offset"),
                {"parent_id": parent_id, "limit": ( page + 1 ) * take, "offset": page * 10}).fetchall()
        
        if not myFriends:
            return None

        # 짝꿍
        mate = db.execute(text(
            f"select f.parent_id from friend p inner join friend f \
            ON p.parent_id = f.friend AND p.friend = f.parent_id \
            where p.parent_id = \"{parent_id}\"")).fetchall()

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

        paginationInfo = {'page': page, 'take': take, 'total': total}
        
        return {
            'paginationInfo': paginationInfo,
            'parents': parents
        }
    


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

        # 유저가 조회한 post 찾기
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

        # 유저가 스크립트한 post 찾기
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

        # 유저가 좋아요 누른 post 찾기
        likes = db.execute(text(
        f"select * from post p inner join pheart h on p.post_id = h.post_id \
            where h.parent_id = :parent_id LIMIT :limit OFFSET :offset"),
            {"parent_id": parent_id, "limit": ( page + 1 ) * take, "offset": page * 10}).fetchall() 

        if not likes:
            return []

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

        total = db.query(PostTable).filter(
            PostTable.parent_id == parent_id,
            PostTable.deleteTime == None).count()

        paginationInfo = {'page': page, 'take': take, 'total': total}

        # 유저의 post 찾기
        myStories = db.execute(text(
        f"SELECT * FROM post WHERE parent_id = :parent_id AND deleteTime IS NULL LIMIT :limit OFFSET :offset"),
            {"parent_id": parent_id, "limit": ( page + 1 ) * take, "offset": page * 10}).fetchall() 

        # 유저 post 데이터
        posts = []
        for i in myStories:
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

        # 짝꿍 수
        total = int(db.execute(text(
            f"select count(0) from friend p inner join friend f \
            ON p.parent_id = f.friend AND p.friend = f.parent_id \
            where p.parent_id = \"{parent_id}\"")).fetchall()[0][0])
        
        paginationInfo = {'page': page, 'take': take, 'total': total}

        # 짝꿍 정보 가져오기
        myMates = db.execute(text(
            f"select p.* from friend fp inner join friend f \
                ON fp.parent_id = f.friend AND fp.friend = f.parent_id \
                inner join parent p on p.parent_id = f.parent_id \
                where fp.parent_id = :parent_id LIMIT :limit OFFSET :offset"),
            {"parent_id": parent_id, "limit": ( page + 1 ) * take, "offset": page * 10}).fetchall()

        if not myMates:
            return []

        # 짝꿍 데이터
        parents = []
        for i in myMates:
            parents.append({
                'parent_id': i[0],
                'nickname': i[4],
                'photoId': i[8],
                'description': i[9]
            })

        return [paginationInfo, parents]