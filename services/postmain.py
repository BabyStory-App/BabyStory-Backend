
import os

from fastapi import HTTPException
from typing import Optional, List
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from sqlalchemy import desc

from model.post import PostTable
from model.friend import FriendTable

from schemas.postmain import *
from db import get_db_session

class PostMainService:

    # 메인 페이지 배너 생성
    def createPostMainBanner(self)->CreatePostMainBannerListOutput:
        """
        메인 페이지 배너 생성
        --output
            - List<{postid, photoId, title, author_name, desc 초반 100자}> : 메인 페이지 배너
        """
        # 오늘 00시부터 하루 전 23시 59분까지의 시간 간격을 계산합니다.
        end = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start = end - timedelta(days=1)
        file_name = str(start).replace(":", "_") + '.txt'

        db = get_db_session()
        try:
            # (start)어제의 날짜.txt 라는 파일이 존재하지 않으면
            if not os.path.exists(str(file_name) + '.txt'):

                # 전날 00시부터 23시 59분까지의 하트를 기준으로 상위 5개의 포스트를 가져옵니다.
                banner = db.query(PostTable).filter(
                    PostTable.createTime <= end,
                    PostTable.createTime >= start
                    ).order_by(desc(PostTable.pHeart)).limit(5).all()

                # 각각의 post_id를 리스트에 저장한다
                post_id_list = []
                for i in banner:
                    post_id_list.append({i.post_id})
                
                # (start)어제의 날짜.txt 파일을 생성합니다.
                with open(str(file_name) + '.txt', 'w') as f:
                    for item in post_id_list:
                        f.write("%s\n" % item)

            # (start)어제의 날짜.txt 파일이 존재하면
            else:
                with open(str(file_name) + '.txt', 'r') as f:
                    post_id_list = f.readlines()

                # post_id_list에 있는 post_id를 이용하여 post를 가져옵니다.
                banner = db.query(PostTable).filter(
                    PostTable.post_id.in_(post_id_list)
                ).all()           

            # banner의 값을 반환:List<{postid, photoId, title, author name, desc 초반 100자}>
            # 이때, desc는 100자로 제한한다.
            banners = []
            for i in banner:
                banners.append({
                    'post_id': i.post_id,
                    'photoId': i.photoId,
                    'title': i.title,
                    'author_name': db.query(ParentTable).filter(
                        ParentTable.parent_id == i.parent_id).first().name,
                    'desc': i.content[:100]
                })

           # post테이블에 제목, 조회수 없음

            return banners
        
        except Exception as e:
            raise (e)
            #raise Exception("Failed to create banner")
        
    def createPostMainFriend(self, createPostMainInput: CreatePostMainInput)->CreatePostMainFriendListOutput:
        """
        짝꿍이 쓴 게시물
        --input
            - createPostMainInput.parent_id: 부모 아이디
            - createPostMainInput.size: 게시물 개수 default -1
            - createPostMainInput.page: 페이지 수 default -1
        --output
            - List<{postid, photoId, title, author_photo, author_name}> : 짝꿍이 쓴 게시물
        """
        db = get_db_session()
        try:
            end = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # size와 page가 -1이면 기본 페이지를 가져온다.
            if createPostMainInput.size == -1 and createPostMainInput.page == -1:
                size = 10
                page = 0
            else:
                size = createPostMainInput.size
                page = (createPostMainInput.page - 1) * 10

            # # 친구 가져오기
            friends = db.query(FriendTable).filter(
                FriendTable.parent_id == createPostMainInput.parent_id
                ).all()
            
            # 짝꿍 : 친구도 나를 친구로 등록했는지 확인
            # 나를 친구로 등록한 사람 가져오기
            temp = db.query(FriendTable).filter(
                    FriendTable.friend == createPostMainInput.parent_id
                ).all()
            
            temp_ids = [friend.parent_id for friend in temp]

            friend = db.query(FriendTable).filter(
                FriendTable.friend.in_(temp_ids)
            ).all()

            friend_ids = [f.parent_id for f in friend]
            
            # 오늘 친구가 쓴 게시물 중 page에서 size개 가져오기
            post = db.query(PostTable).filter(
                PostTable.parent_id.in_(friend_ids),
                PostTable.createTime >= end
                ).order_by(desc(PostTable.createTime)).limit(size).offset(page).all()


            # 값을 반환: List<{postid, photoId, title, author_photo, author_name}>
            banners = []
            for i in post:
                banners.append({
                    'post_id': i.post_id,
                    'photoId': i.photoId,
                    'title': i.title,
                    'author_photo': db.query(ParentTable).filter(
                        ParentTable.parent_id == i.parent_id).first().photoId,
                    'author_name': db.query(ParentTable).filter(
                        ParentTable.parent_id == i.parent_id).first().name
                })

            return banners
        
        except Exception as e:
            raise (e)
            #raise Exception("Failed to create friend banner")


    def createPostMainFriendRead(self,createPostMainInput: CreatePostMainInput)->CreatePostMainFriendListOutput:
        """
        친구가 쓴 게시물
        --input
            - createPostMainInput.parent_id: 부모 아이디
            - createPostMainInput.size: 게시물 개수 default -1
            - createPostMainInput.page: 페이지 수 default -1
        --output
            - List<{postid, photoId, title, pHeart, comment, author_name, desc}> : 친구가 쓴 게시물
        """
        db = get_db_session()
        try:
            # 어제 시간
            end = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            
            # size와 page가 -1이면 기본 페이지를 가져온다.
            if createPostMainInput.size == -1 and createPostMainInput.page == -1:
                size = 10
                page = 0
            else:
                size = createPostMainInput.size
                page = (createPostMainInput.page - 1) * 10

            # 친구 가져오기
            friend = db.query(FriendTable).filter(
                FriendTable.parent_id == createPostMainInput.parent_id
                ).all()

            friend_ids = [f.friend for f in friend]

            # 친구가 쓴 게시물 중 page에서 size개 가져오기
            post = db.query(PostTable).filter(
                PostTable.parent_id.in_(friend_ids),
                PostTable.createTime >= end
                ).order_by(desc(PostTable.createTime)).limit(size).offset(page).all()

            # 값을 반환: List<{postid, photoId, title, pHeart, comment, author_name, desc}>
            banners = []
            for i in post:
                banners.append({
                    'post_id': i.post_id,
                    'photoId': i.photoId,
                    'title': i.title,
                    'pHeart': i.pHeart,
                    'comment': i.pComment,
                    'author_name': db.query(ParentTable).filter(
                        ParentTable.parent_id == i.parent_id).first().name,
                    'desc': i.content[:100]
                })

            return banners
        
        except Exception as e:
            raise (e)
            #raise Exception("Failed to create friend read")

    def getNeighbor(self, parent_id: str)->GetNeighborOutputListOutput:
        """
        친구로 등록되지 않은 이웃목록
        --input
            - parent_id: 부모 아이디
        --output
            - List<{parent_id, photoId, name, mainAddr, desc}> : 친구로 등록되지 않은 이웃목록
        """

        db = get_db_session()
        try:
            # 친구로 등록되지 않은 이웃목록을 10개 가져오기
            neighbors = db.query(ParentTable).filter(
                ParentTable.parent_id != parent_id,
                ParentTable.parent_id not in db.query(FriendTable.friend).filter(
                    FriendTable.parent_id == parent_id
                ),
                ParentTable.mainAddr == db.query(ParentTable.mainAddr).filter(
                    ParentTable.parent_id == parent_id
                )
            ).limit(10).all()


            # 값을 반환: List<{parent_id, photoId, name, mainAddr, desc}>
            banners = []
            for i in neighbors:
                banners.append({
                    'parent_id': i.parent_id,
                    'photoId': i.photoId,
                    'name': i.name,
                    'mainAddr': i.mainAddr,
                    'desc': i.description
                })

            return banners
        
        except Exception as e:
            raise (e)
            #raise Exception("Failed to get neighbor list")


    def createPostMainNeighbor(self, createPostMainInput: CreatePostMainInput )->CreatePostMainNeighborListOutput:
        """
        이웃들이 쓴 게시물
        --input
            - createPostMainInput.parent_id: 부모 아이디
            - createPostMainInput.size: 게시물 개수 default -1
            - createPostMainInput.page: 페이지 수 default -1
        --output
            - List<{postid, photoId, title, pHeart, comment, author_name, desc}> : 이웃이 쓴 게시물
        """
        db = get_db_session()
        try:
            # size와 page가 -1이면 기본 페이지를 가져온다.
            if createPostMainInput.size == -1 and createPostMainInput.page == -1:
                size = 10
                page = 0
            else:
                size = createPostMainInput.size
                page = (createPostMainInput.page - 1) * 10

            # 이웃을 가져오기
            neighbors = db.query(ParentTable).filter(
                ParentTable.parent_id != createPostMainInput.parent_id,
                ParentTable.mainAddr == db.query(ParentTable.mainAddr).filter(
                    ParentTable.parent_id == createPostMainInput.parent_id
                )
            ).all()

            # 이웃이 쓴 게시물 중 page에서 size개 가져오기
            post = db.query(PostTable).filter(
                PostTable.parent_id.in_([i.parent_id for i in neighbors])
            ).order_by(desc(PostTable.createTime)).limit(size).offset(page).all()

            # 값을 반환: List<{postid, photoId, title, pHeart, comment, author_name, desc}>
            banners = []
            for i in post:
                banners.append({
                    'post_id': i.post_id,
                    'photoId': i.photoId,
                    'title': i.title,
                    'pHeart': i.pHeart,
                    'comment': i.pComment,
                    'author_name': db.query(ParentTable).filter(
                        ParentTable.parent_id == i.parent_id).first().name,
                    'desc': i.content[:100]
                })

            return banners
        
        except Exception as e:
            raise (e)
            #raise Exception("Failed to create neighbor banner")

    def createPostMainHighView(self)->CreatePostMainHighViewListOutput:

        """
        조회수가 높은 게시물
        --output
            - List<{postid, photoId, title, author_name, desc}> : 조회수가 높은 게시물
        """
        db = get_db_session()
        try:
            # 조회수가 높은 게시물을 가져옵니다.
            post = db.query(PostTable).order_by(desc(PostTable.pView)).limit(10).all()

            # 값을 반환: List<{postid, photoId, title, author_name, desc}>
            banners = []
            for i in post:
                banners.append({
                    'post_id': i.post_id,
                    'photoId': i.photoId,
                    'title': i.title,
                    'author_name': db.query(ParentTable).filter(
                        ParentTable.parent_id == i.parent_id).first().name,
                    'desc': i.content[:100]
                })


            return banners
        
        except Exception as e:
            raise (e)
            #raise Exception("Failed to create high view banner")
    
    def createPostMainHashtag(self, parent_id:str)->CreatePostMainHashtagListOutput:

        """
        많이 본 해시태그로 게시물 추천
        --input
            - parent_id: 부모 아이디
        --output
            - List<{postid, photoId, title, author_name, desc, hashList}> : 많이 본 해시태그로 게시물 추천
        """
        db = get_db_session()
        try:
            # 부모 테이블에 많이본 해시태그가 몇 개 있고 그게 포함된 게시물을 가져오기
            parent = db.query(ParentTable).filter(
                ParentTable.parent_id == parent_id
            ).first()

            # 부모가 없거나 해시태그가 없으면 빈 리스트 반환
            if not parent or not parent.hashList:
                return []

            parent_hashlist = parent.hashList.split(',')

            # 최신순 게시물을 가져오기
            posts = db.query(PostTable).order_by(PostTable.createTime.desc()).all()
            matching_posts = []

            # 해시태그가 포함된 게시물을 가져오기
            for post in posts:
                post_hashlist = post.hashList.split(',')
                if any(hash in parent_hashlist for hash in post_hashlist):
                    matching_posts.append(post)
                if len(matching_posts) == 10:
                    break

            # 값을 반환: List<{postid, photoId, title, author_name, desc, hashList}>
            banners = []
            for post in matching_posts:
                author_name = db.query(ParentTable).filter(
                    ParentTable.parent_id == post.parent_id).first().name
                banners.append({
                    'post_id': post.post_id,
                    'photoId': post.photoId,
                    'title': post.title,
                    'author_name': author_name,
                    'desc': post.content[:100],
                    'hash': post.hashList
                })

            return banners
        
        except Exception as e:
            raise (e)
            #raise Exception("Failed to create hashtag banner")
