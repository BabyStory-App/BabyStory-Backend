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

        # 오늘 00시부터 하루 전 23시 59분까지의 시간 간격을 계산합니다.
        end = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start = end - timedelta(days=1)

        db = get_db_session()
        try:
            # (start)어제의 날짜.txt 라는 파일이 존재하지 않으면
            if not os.path.exists(str(start) + '.txt'):

                # 전날 00시부터 23시 59분까지의 하트를 기준으로 상위 5개의 포스트를 가져옵니다.
                banner = db.query(PostTable).filter(
                    PostTable.post_time <= end,
                    PostTable.post_time >= start
                    ).order_by(desc(PostTable.heart)).limit(5).all()

                # 각각의 post_id를 리스트에 저장한다
                post_id_list = []
                for i in banner:
                    post_id_list.append({i.post_id})
                
                # (start)어제의 날짜.txt 파일을 생성합니다.
                with open(str(start) + '.txt', 'w') as f:
                    for item in post_id_list:
                        f.write("%s\n" % item)

            # (start)어제의 날짜.txt 파일이 존재하면
            else:
                with open(str(start) + '.txt', 'r') as f:
                    post_id_list = f.readlines()

                # post_id_list에 있는 post_id를 이용하여 post를 가져옵니다.
                banner = db.query(PostTable).filter(
                    PostTable.post_id.in_(post_id_list)
                ).all()           

            # banner의 값을 반환:List<{postid, photoid, title, author name, desc 초반 100자}>
            # 이때, desc는 100자로 제한한다.
            banners = []
            for i in banner:
                banners.append({
                    'post_id': i.post_id,
                    'photo_id': i.photos,
                    'title': i.title,
                    'author_name': db.query(ParentTable).filter(
                        ParentTable.parent_id == i.parent_id).first().name,
                    'desc': i.post[:100]
                })

            return banners
        
        except Exception as e:
            raise (e)
            #raise Exception("Failed to create banner")
        
    def createPostMainFriend(self, parent_id: str, size: int =-1, page: int =-1)->CreatePostMainFriendListOutput:
        db = get_db_session()
        try:
            end = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # size와 page가 -1이면 기본 페이지를 가져온다.
            if size == -1 and page == -1:
                size = 10
                page = 0
            else:
                page = (page - 1) * 10

            # 친구 가져오기
            friends = db.query(FriendTable).filter(
                FriendTable.parent_id1 == parent_id
                ).all()
            
            # 짝꿍 : 친구도 나를 친구로 등록했는지 확인
            friend = db.query(FriendTable).filter(
                db.query(FriendTable).filter(
                    FriendTable.parent_id2 == parent_id
                ).first().parent_id1 in friends.parent_id2
                ).all()

            
            # 오늘 친구가 쓴 게시물 중 page에서 size개 가져오기
            post = db.query(PostTable).filter(
                PostTable.parent_id == friend.parent_id2,
                PostTable.post_time >= end
                ).order_by(desc(PostTable.post_time)).limit(size).offset(page).all()


            # 값을 반환: List<{postid, photoid, title, author_photo, author_name}>
            banners = []
            for i in post:
                banners.append({
                    'post_id': i.post_id,
                    'photo_id': i.photos,
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


    def createPostMainFriendRead(self,parent_id: str, size: int =-1, page: int =-1)->CreatePostMainFriendListOutput:
        db = get_db_session()
        try:
            # 어제 시간
            end = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            # size와 page가 -1이면 기본 페이지를 가져온다.
            if size == -1 and page == -1:
                size = 10
                page = 0
            else:
                page = (page - 1) * 10

            # 친구 가져오기
            friend = db.query(FriendTable).filter(
                FriendTable.parent_id1 == parent_id
                ).all()

            # 친구가 쓴 게시물 중 page에서 size개 가져오기
            post = db.query(PostTable).filter(
                PostTable.parent_id == friend.parent_id2,
                PostTable.post_time >= end
                ).order_by(desc(PostTable.post_time)).limit(size).offset(page).all()

            # 값을 반환: List<{postid, photoid, title, heart, comment, author_name, desc}>
            banners = []
            for i in post:
                banners.append({
                    'post_id': i.post_id,
                    'photo_id': i.photos,
                    'title': i.title,
                    'heart': i.heart,
                    'comment': i.comment,
                    'author_name': db.query(ParentTable).filter(
                        ParentTable.parent_id == i.parent_id).first().name,
                    'desc': i.post[:100]
                })

            return banners
        
        except Exception as e:
            raise (e)
            #raise Exception("Failed to create friend read")

    def getNeighbor(self, parent_id: str)->GetNeighborOutputListOutput:
        db = get_db_session()
        try:
            # 친구로 등록되지 않은 이웃목록을 10개 가져오기
            neighbors = db.query(ParentTable).filter(
                ParentTable.parent_id != parent_id,
                ParentTable.parent_id not in db.query(FriendTable.parent_id2).filter(
                    FriendTable.parent_id1 == parent_id
                ),
                ParentTable.mainaddr == db.query(ParentTable.mainaddr).filter(
                    ParentTable.parent_id == parent_id
                )
            ).limit(10).all()

            # 값을 반환: List<{parent_id, photo_id, name, mainaddr, desc}>
            banners = []
            for i in neighbors:
                banners.append({
                    'parent_id': i.parent_id,
                    'photo_id': i.photoId,
                    'name': i.name,
                    'mainaddr': i.mainaddr,
                    'desc': i.description
                })


            return banners
        
        except Exception as e:
            raise (e)
            #raise Exception("Failed to get neighbor list")

    def createPostMainNeighbor(self, parent_id: str, size: int =-1, page: int =-1 )->CreatePostMainNeighborListOutput:
        db = get_db_session()
        try:
            # size와 page가 -1이면 기본 페이지를 가져온다.
            if size == -1 and page == -1:
                size = 10
                page = 0
            else:
                page = (page - 1) * 10

            # 이웃을 가져오기
            neighbors = db.query(ParentTable).filter(
                ParentTable.parent_id != parent_id,
                ParentTable.mainaddr == db.query(ParentTable.mainaddr).filter(
                    ParentTable.parent_id == parent_id
                )
            ).all()

            # 이웃이 쓴 게시물 중 page에서 size개 가져오기
            post = db.query(PostTable).filter(
                PostTable.parent_id.in_([i.parent_id for i in neighbors])
            ).order_by(desc(PostTable.post_time)).limit(size).offset(page).all()

            # 값을 반환: List<{postid, photoid, title, heart, comment, author_name, desc}>
            banners = []
            for i in post:
                banners.append({
                    'post_id': i.post_id,
                    'photo_id': i.photos,
                    'title': i.title,
                    'heart': i.heart,
                    'comment': i.comment,
                    'author_name': db.query(ParentTable).filter(
                        ParentTable.parent_id == i.parent_id).first().name,
                    'desc': i.post[:100]
                })

            return banners
        
        except Exception as e:
            raise (e)
            #raise Exception("Failed to create neighbor banner")

    def createPostMainHighView(self)->CreatePostMainHighViewListOutput:
        db = get_db_session()
        try:
            # 조회수가 높은 게시물을 가져옵니다.
            post = db.query(PostTable).order_by(desc(PostTable.view)).limit(10).all()

            # 값을 반환: List<{postid, photoid, title, author_name, desc}>
            banners = []
            for i in post:
                banners.append({
                    'post_id': i.post_id,
                    'photo_id': i.photos,
                    'title': i.title,
                    'author_name': db.query(ParentTable).filter(
                        ParentTable.parent_id == i.parent_id).first().name,
                    'desc': i.post[:100]
                })


            return banners
        
        except Exception as e:
            raise (e)
            #raise Exception("Failed to create high view banner")
    
    def createPostMainHashtag(self, parent_id:str)->CreatePostMainHashtagListOutput:
        db = get_db_session()
        try:
            # 부모 테이블에 많이본 해시태그가 몇 개 있고 그게 포함된 게시물을 가져오기
            parent = db.query(ParentTable).filter(
                ParentTable.parent_id == parent_id
            ).first()

            hash = parent.hash.split(',')

            # 해시태그가 포함된 게시물을 가져오기
            post = db.query(PostTable).filter(
                PostTable.hash.in_(hash)
            ).order_by(desc(PostTable.view)).limit(10).all()

            # 값을 반환: List<{postid, photoid, title, author_name, desc, hash}>
            banners = []
            for i in post:
                banners.append({
                    'post_id': i.post_id,
                    'photo_id': i.photos,
                    'title': i.title,
                    'author_name': db.query(ParentTable).filter(
                        ParentTable.parent_id == i.parent_id).first().name,
                    'desc': i.post[:100],
                    'hash': i.hash
                })

            return banners
        
        except Exception as e:
            raise (e)
            #raise Exception("Failed to create hashtag banner")

# post에 조회수 없음
# parent에 hash 없음
