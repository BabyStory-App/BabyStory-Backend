import os
from constants.path import *
from fastapi import HTTPException
from constants.path import *
import re
import random

from datetime import datetime, timedelta
from sqlalchemy import desc

from model.post import PostTable
from model.friend import FriendTable
from model.pheart import PHeartTable

from schemas.postmain import *
from db import get_db_session

from error.exception.customerror import *


class PostMainService:

    def _get_photoId_and_desc(self, content: str):
        # content에 ![[Image1.jpeg]] 형식의 이미지가 있으면 첫번째 이미지 경로를 가져온다.
        photoIdRex = re.search(r'!\[\[(.*?)\]\]', content)
        photoId = photoIdRex.group(1) if photoIdRex else None

        # 위처럼 개행, 이미지 경로는 제거하고 100자로 자른다.
        content = re.sub(r'!\[\[(.*?)\]\]', '', content)
        descr = content if len(
            content) < 100 else content[:100] + '...'

        return photoId, descr

    # 메인 페이지 배너 생성
    def createPostMainBanner(self) -> CreatePostMainBannerListOutput:
        """
        메인 페이지 배너 생성
        --output
            - List<{postid, photoId, title, author_name, desc 초반 100자}> : 메인 페이지 배너
        """
        # 임시로 설정함.
        db = get_db_session()
        posts = db.query(PostTable).order_by(
            desc(PostTable.pHeart)).all()
        banners = []
        idx = 0
        for i in posts:
            # POST_CONTENT_DIR에 있는 파일 중 post_id경로의 content를 읽어온다.
            file_path = os.path.join(
                POST_CONTENT_DIR, str(i.post_id) + '.txt')
            with open(file_path, 'r', encoding='UTF-8') as f:
                content = f.read()

            # content에 ![[Image1.jpeg]] 형식의 이미지가 있으면 첫번째 이미지 경로를 가져온다.
            photoId = re.search(r'!\[\[(.*?)\]\]', content)
            if photoId:
                photoId = photoId.group(1)

                # 위처럼 개행, 이미지 경로는 제거하고 100자로 자른다.
                content = re.sub(r'!\[\[(.*?)\]\]', '', content)
                descr = content if len(
                    content) < 100 else content[:100] + '...'
                banners.append({
                    'postid': i.post_id,
                    'photoId': photoId,
                    'title': i.title,
                    'author_name': db.query(ParentTable).filter(ParentTable.parent_id == i.parent_id).first().name,
                    'desc': descr
                })
                idx += 1
            if idx == 5:
                break

        return banners
        # 실제 코드
        # 오늘 00시부터 하루 전 23시 59분까지의 시간 간격을 계산합니다.
        end = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start = end - timedelta(days=1)
        file_name = str(start).replace(":", "_") + '.txt'

        db = get_db_session()

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
            file_path = os.path.join(
                POSTMAIN_BANNER_DIR, str(file_name) + '.txt')
            with open(file_path, 'w', encoding='UTF-8') as f:
                for item in post_id_list:
                    f.write("%s\n" % item)

        # (start)어제의 날짜.txt 파일이 존재하면
        else:
            file_path = os.path.join(
                POSTMAIN_BANNER_DIR, str(file_name) + '.txt')
            with open(file_path, 'r') as f:
                post_id_list = [int(line.strip('{}\n'))
                                for line in f.readlines()]

            # post_id_list에 있는 post_id를 이용하여 post를 가져옵니다.
            banner = db.query(PostTable).filter(
                PostTable.post_id.in_(post_id_list)
            ).all()

        # banner의 값을 반환:List<{postid, photoId, title, author name, desc 초반 100자}>
        # 이때, desc는 100자로 제한한다.
        banners = []
        for i in banner:
            # POST_CONTENT_DIR에 있는 파일 중 post_id경로의 content를 읽어온다.
            file_path = os.path.join(
                POST_CONTENT_DIR, str(i.post_id) + '.txt')
            with open(file_path, 'r', encoding='UTF-8') as f:
                content = f.read()

            # 위처럼 개행, 이미지 경로는 제거하고 100자로 자른다.
            content = re.sub(r'!\[\[(.*?)\]\]', '', content)
            content = re.sub(r'\n', '', content)
            if len(content) >= 100:
                descr = content[:100] + '...'
            else:
                descr = content

            # content에 ![[Image1.jpeg]] 형식의 이미지가 있으면 첫번째 이미지 경로를 가져온다.
            photoId = re.search(r'!\[\[(.*?)\]\]', content)
            if photoId:
                photoId = photoId.group(1)
            else:
                photoId = None

            banners.append({
                'post_id': i.post_id,
                'photoId': photoId,
                'title': i.title,
                'author_name': db.query(ParentTable).filter(
                    ParentTable.parent_id == i.parent_id).first().name,
                'desc': descr
            })

        return banners

    def createPostMainFriend(self, createPostMainInput: CreatePostMainInput) -> CreatePostMainFriendListOutput:
        """
        짝꿍이 쓴 게시물
        --input
            - createPostMainInput.parent_id: 부모 아이디
            - createPostMainInput.size: 게시물 개수 default -1
            - createPostMainInput.page: 페이지 수 default -1
        --output
            - List<{postid, photoId, title, author_photo, author_name}> : 짝꿍이 쓴 게시물
        """
        # 임시로 설정함.
        db = get_db_session()
        posts = db.query(PostTable).all()
        random.shuffle(posts)
        idx = 0
        banners = []
        for i in posts:
            photo_file_list = os.listdir(os.path.join(
                POST_PHOTO_DIR, str(i.post_id)))
            if len(photo_file_list) > 0:
                # 유저가 게시물에 하트를 눌렀는지 확인
                hasHeart = False
                if db.query(PHeartTable).filter(
                    PHeartTable.parent_id == createPostMainInput.parent_id,
                    PHeartTable.post_id == i.post_id
                ).first() is not None:
                    hasHeart = True
                banners.append({
                    'postid': i.post_id,
                    'photoId': f"{photo_file_list[0]}",
                    'hasHeart': hasHeart,
                    'title': i.title,
                    'author_photo': f"{i.parent_id}",
                    'author_name': db.query(ParentTable).filter(ParentTable.parent_id == i.parent_id).first().name
                })
                idx += 1
            if idx == 5:
                break
        return banners

        # 실제 코드
        db = get_db_session()

        end = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end = end - timedelta(days=1)

        if createPostMainInput.size != -1 and createPostMainInput.size < 0:
            raise CustomException("size must be -1 or greater than 0")
        if createPostMainInput.page != -1 and createPostMainInput.page < 0:
            raise CustomException("page must be -1 or greater than 0")

        # size와 page가 -1이면 기본 페이지를 가져온다.
        if createPostMainInput.size == -1 or createPostMainInput.size == 0:
            size = 10
        else:
            size = createPostMainInput.size

        if createPostMainInput.page == -1 or createPostMainInput.page == 0:
            page = 0
        else:
            # 10개씩 보여주는 페이지일 경우 페이지의 시작점을 계산
            page = createPostMainInput.page * size

        temp = db.query(FriendTable).filter(
            FriendTable.friend == createPostMainInput.parent_id
        ).all()

        temp_ids = [friend.parent_id for friend in temp]

        friend = db.query(FriendTable).filter(
            FriendTable.parent_id == createPostMainInput.parent_id,
            FriendTable.friend.in_(temp_ids)
        ).all()

        friend_ids = [f.friend for f in friend]

        # 오늘 친구가 쓴 게시물 중 page에서 size개 가져오기
        post = db.query(PostTable).filter(
            PostTable.parent_id.in_(friend_ids),
            PostTable.createTime >= end
        ).order_by(desc(PostTable.createTime)).offset(page).limit(size).all()

        # 값을 반환: List<{postid, photoId, title, parentHeart, author_photo, author_name}>
        banners = []
        for i in post:
            # file_list = os.listdir(os.path.join(
            #     POST_PHOTO_DIR, str(i.post_id)))
            # if len(file_list) == 0:
            #     photoId = None
            # else:
            #     # file_list의 첫번째 이미지를 photoId 경로로 사용
            #     photoId = os.path.join(
            #         POST_PHOTO_DIR, str(i.post_id), file_list[0])
            # POST_CONTENT_DIR에 있는 파일 중 post_id경로의 content를 읽어온다.
            file_path = os.path.join(
                POST_CONTENT_DIR, str(i.post_id) + '.txt')
            with open(file_path, 'r', encoding='UTF-8') as f:
                content = f.read()

            # content에 ![[Image1.jpeg]] 형식의 이미지가 있으면 첫번째 이미지 경로를 가져온다.
            photoId = re.search(r'!\[\[(.*?)\]\]', content)
            if photoId:
                photoId = photoId.group(1)
            else:
                photoId = None

            # 유저가 게시물에 하트를 눌렀는지 확인
            if db.query(PHeartTable).filter(
                PHeartTable.parent_id == createPostMainInput.parent_id,
                PHeartTable.post_id == i.post_id
            ).first() is not None:
                pHeart = True
            else:
                pHeart = False

            banners.append({
                'post_id': i.post_id,
                'photoId': photoId,
                'title': i.title,
                # 'pHeart': i.pHeart,
                'parentHeart': pHeart,
                'author_photo': f"{i.parent_id}.jpeg",
                'author_name': db.query(ParentTable).filter(
                    ParentTable.parent_id == i.parent_id).first().name
            })

        return banners

    def createPostMainFriendSearch(self, createPostMainInput: CreatePostMainInput) -> CreatePostMainFriendSearchListOutput:
        """
        짝꿍이 쓴 게시물
        --input
            - createPostMainInput.parent_id: 부모 아이디
            - createPostMainInput.size: 게시물 개수 default -1
            - createPostMainInput.page: 페이지 수 default -1
        --output
            - List<{postid, photoId, title, author_photo, author_name}> : 짝꿍이 쓴 게시물
        """
        # 임시로 설정함.
        db = get_db_session()
        _data = db.query(PostTable).all()
        posts = random.sample(_data, len(_data) if len(_data) < 5 else 5)
        banners = []
        for i in posts:
            # POST_CONTENT_DIR에 있는 파일 중 post_id경로의 content를 읽어온다.
            file_path = os.path.join(
                POST_CONTENT_DIR, str(i.post_id) + '.txt')
            with open(file_path, 'r', encoding='UTF-8') as f:
                content = f.read()

            photoId, descr = self._get_photoId_and_desc(content)

            banners.append({
                'postid': i.post_id,
                'photoId': photoId,
                'title': i.title,
                'pHeart': i.pHeart,
                'comment': i.pComment,
                'author_name': db.query(ParentTable).filter(ParentTable.parent_id == i.parent_id).first().name,
                'desc': descr
            })
        return banners

        # 실제 코드
        db = get_db_session()

        end = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end = end - timedelta(days=1)

        if createPostMainInput.size != -1 and createPostMainInput.size < 0:
            raise CustomException("size must be -1 or greater than 0")
        if createPostMainInput.page != -1 and createPostMainInput.page < 0:
            raise CustomException("page must be -1 or greater than 0")

        # size와 page가 -1이면 기본 페이지를 가져온다.
        if createPostMainInput.size == -1 or createPostMainInput.size == 0:
            size = 10
        else:
            size = createPostMainInput.size

        if createPostMainInput.page == -1 or createPostMainInput.page == 0:
            page = 0
        else:
            # 10개씩 보여주는 페이지일 경우 페이지의 시작점을 계산
            page = createPostMainInput.page * size

        temp = db.query(FriendTable).filter(
            FriendTable.friend == createPostMainInput.parent_id
        ).all()

        temp_ids = [friend.parent_id for friend in temp]

        friend = db.query(FriendTable).filter(
            FriendTable.parent_id == createPostMainInput.parent_id,
            FriendTable.friend.in_(temp_ids)
        ).all()

        friend_ids = [f.friend for f in friend]

        # 오늘 친구가 쓴 게시물 중 page에서 size개 가져오기
        post = db.query(PostTable).filter(
            PostTable.parent_id.in_(friend_ids),
            PostTable.createTime >= end
        ).order_by(desc(PostTable.createTime)).offset(page).limit(size).all()

        # 값을 반환: List<{postid, photoId, title, parentHeart, author_photo, author_name}>
        banners = []
        for i in post:
            # file_list = os.listdir(os.path.join(
            #     POST_PHOTO_DIR, str(i.post_id)))
            # if len(file_list) == 0:
            #     photoId = None
            # else:
            #     # file_list의 첫번째 이미지를 photoId 경로로 사용
            #     photoId = os.path.join(
            #         POST_PHOTO_DIR, str(i.post_id), file_list[0])
            # POST_CONTENT_DIR에 있는 파일 중 post_id경로의 content를 읽어온다.
            file_path = os.path.join(
                POST_CONTENT_DIR, str(i.post_id) + '.txt')
            with open(file_path, 'r', encoding='UTF-8') as f:
                content = f.read()

            # content에 ![[Image1.jpeg]] 형식의 이미지가 있으면 첫번째 이미지 경로를 가져온다.
            photoId = re.search(r'!\[\[(.*?)\]\]', content)
            if photoId:
                photoId = photoId.group(1)
            else:
                photoId = None

            # 유저가 게시물에 하트를 눌렀는지 확인
            if db.query(PHeartTable).filter(
                PHeartTable.parent_id == createPostMainInput.parent_id,
                PHeartTable.post_id == i.post_id
            ).first() is not None:
                pHeart = True
            else:
                pHeart = False

            banners.append({
                'post_id': i.post_id,
                'photoId': photoId,
                'title': i.title,
                # 'pHeart': i.pHeart,
                'parentHeart': pHeart,
                'author_photo': f"{i.parent_id}.jpeg",
                'author_name': db.query(ParentTable).filter(
                    ParentTable.parent_id == i.parent_id).first().name
            })

        return banners

    def createPostMainFriendRead(self, createPostMainInput: CreatePostMainInput) -> CreatePostMainFriendListOutput:
        """
        친구가 쓴 게시물
        --input
            - createPostMainInput.parent_id: 부모 아이디
            - createPostMainInput.size: 게시물 개수 default -1
            - createPostMainInput.page: 페이지 수 default -1
        --output
            - List<{postid, photoId, title, pHeart, comment, author_name, desc}> : 친구가 쓴 게시물
        """
        # 임시로 설정함.
        db = get_db_session()
        _data = db.query(PostTable).all()
        posts = random.sample(_data, len(_data) if len(_data) < 5 else 5)
        banners = []
        for i in posts:
            # POST_CONTENT_DIR에 있는 파일 중 post_id경로의 content를 읽어온다.
            file_path = os.path.join(
                POST_CONTENT_DIR, str(i.post_id) + '.txt')
            with open(file_path, 'r', encoding='UTF-8') as f:
                content = f.read()

            photoId, descr = self._get_photoId_and_desc(content)

            banners.append({
                'postid': i.post_id,
                'photoId': photoId,
                'title': i.title,
                'pHeart': i.pHeart,
                'comment': i.pComment,
                'author_name': db.query(ParentTable).filter(ParentTable.parent_id == i.parent_id).first().name,
                'desc': descr
            })
        return banners

        # 실제 코드
        db = get_db_session()

        # 어제 시간
        end = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # 어제 시간
        end = end - timedelta(days=1)

        if createPostMainInput.size != -1 and createPostMainInput.size < 0:
            raise CustomException("size must be -1 or greater than 0")
        if createPostMainInput.page != -1 and createPostMainInput.page < 0:
            raise CustomException("page must be -1 or greater than 0")

        # size와 page가 -1이면 기본 페이지를 가져온다.
        if createPostMainInput.size == -1 or createPostMainInput.size == 0:
            size = 10
        else:
            size = createPostMainInput.size

        if createPostMainInput.page == -1 or createPostMainInput.page == 0:
            page = 0
        else:
            # 10개씩 보여주는 페이지일 경우 페이지의 시작점을 계산
            page = createPostMainInput.page * size

        # 친구 가져오기
        friend = db.query(FriendTable).filter(
            FriendTable.parent_id == createPostMainInput.parent_id
        ).all()

        friend_ids = [f.friend for f in friend]

        # 친구가 쓴 게시물 중 page에서 size개 가져오기
        post = db.query(PostTable).filter(
            PostTable.parent_id.in_(friend_ids),
            PostTable.createTime >= end
        ).order_by(desc(PostTable.createTime)).offset(page).limit(size).all()

        # 값을 반환: List<{postid, photoId, title, pHeart, comment, author_name, desc}>
        banners = []
        for i in post:
            # POST_CONTENT_DIR에 있는 파일 중 post_id경로의 content를 읽어온다.
            file_path = os.path.join(
                POST_CONTENT_DIR, str(i.post_id) + '.txt')
            with open(file_path, 'r', encoding='UTF-8') as f:
                content = f.read()

            # 위처럼 개행, 이미지 경로는 제거하고 100자로 자른다.
            content = re.sub(r'!\[\[(.*?)\]\]', '', content)
            content = re.sub(r'\n', '', content)
            if len(content) >= 100:
                descr = content[:100] + '...'
            else:
                descr = content

            # content에 ![[Image1.jpeg]] 형식의 이미지가 있으면 첫번째 이미지 경로를 가져온다.
            photoId = re.search(r'!\[\[(.*?)\]\]', content)
            if photoId:
                photoId = photoId.group(1)
            else:
                photoId = None

            banners.append({
                'post_id': i.post_id,
                'photoId': photoId,
                'title': i.title,
                'pHeart': i.pHeart,
                'comment': i.pComment,
                'author_name': db.query(ParentTable).filter(
                    ParentTable.parent_id == i.parent_id).first().name,
                'desc': descr
            })

        return banners

    def getNeighbor(self, parent_id: str) -> GetNeighborOutputListOutput:
        """
        친구로 등록되지 않은 이웃목록
        --input
            - parent_id: 부모 아이디
        --output
            - List<{parent_id, photoId, name, mainAddr, desc}> : 친구로 등록되지 않은 이웃목록
        """
        # 임시로 설정함.
        db = get_db_session()
        _data = db.query(ParentTable).all()
        neighbors = random.sample(_data, len(_data) if len(_data) < 10 else 10)
        banners = []
        for i in neighbors:
            banners.append({
                'parent_id': i.parent_id,
                'photoId': f"{i.parent_id}",
                'name': i.name,
                'mainAddr': i.mainAddr,
                'desc': i.description[:100]
            })
        return banners

        # 실제 코드

        db = get_db_session()

        # 친구로 등록한 목록
        friend = db.query(FriendTable).filter(
            FriendTable.parent_id == parent_id
        ).all()

        friend_ids = [f.friend for f in friend]

        # 친구로 등록되지 않은 이웃목록을 10개 가져오기
        neighbors = db.query(ParentTable).filter(
            ParentTable.parent_id != parent_id,
            ParentTable.parent_id.notin_(friend_ids)  # 친구로 등록되지 않은 이웃
            ,
            ParentTable.mainAddr == db.query(ParentTable.mainAddr).filter(
                ParentTable.parent_id == parent_id
            )
        ).limit(10).all()

        # 값을 반환: List<{parent_id, photoId, name, mainAddr, desc}>
        banners = []
        for i in neighbors:
            banners.append({
                'parent_id': i.parent_id,
                'photoId': f"{i.parent_id}.jpeg",
                'name': i.name,
                'mainAddr': i.mainAddr,
                'desc': i.description[:60] + '...'
            })

        return banners

    def createPostMainNeighbor(self, createPostMainInput: CreatePostMainInput) -> CreatePostMainNeighborListOutput:
        """
        이웃들이 쓴 게시물
        --input
            - createPostMainInput.parent_id: 부모 아이디
            - createPostMainInput.size: 게시물 개수 default -1
            - createPostMainInput.page: 페이지 수 default -1
        --output
            - List<{postid, photoId, title, pHeart, comment, author_name, desc}> : 이웃이 쓴 게시물
        """
        # 임시로 설정함.
        db = get_db_session()
        _data = db.query(PostTable).all()
        posts = random.sample(_data, len(_data) if len(_data) < 5 else 5)
        banners = []
        for i in posts:
            # POST_CONTENT_DIR에 있는 파일 중 post_id경로의 content를 읽어온다.
            file_path = os.path.join(
                POST_CONTENT_DIR, str(i.post_id) + '.txt')
            with open(file_path, 'r', encoding='UTF-8') as f:
                content = f.read()

            photoId, descr = self._get_photoId_and_desc(content)

            banners.append({
                'postid': i.post_id,
                'photoId': photoId,
                'title': i.title,
                'pHeart': i.pHeart,
                'comment': i.pComment,
                'author_name': db.query(ParentTable).filter(ParentTable.parent_id == i.parent_id).first().name,
                'desc': descr
            })
        return banners

        # 실제 코드
        db = get_db_session()
        if createPostMainInput.size != -1 and createPostMainInput.size < 0:
            raise CustomException("size must be -1 or greater than 0")
        if createPostMainInput.page != -1 and createPostMainInput.page < 0:
            raise CustomException("page must be -1 or greater than 0")

        # size와 page가 -1이면 기본 페이지를 가져온다.
        if createPostMainInput.size == -1 or createPostMainInput.size == 0:
            size = 10
        else:
            size = createPostMainInput.size

        if createPostMainInput.page == -1 or createPostMainInput.page == 0:
            page = 0
        else:
            # 10개씩 보여주는 페이지일 경우 페이지의 시작점을 계산
            page = createPostMainInput.page * size

        # 이웃을 가져오기
        neighbors = db.query(ParentTable).filter(
            ParentTable.parent_id != createPostMainInput.parent_id,
            ParentTable.mainAddr == db.query(ParentTable.mainAddr).filter(
                ParentTable.parent_id == createPostMainInput.parent_id
            ).scalar()
        ).all()

        # 이웃이 쓴 게시물 중 page에서 size개 가져오기
        post = db.query(PostTable).filter(
            PostTable.parent_id.in_([i.parent_id for i in neighbors])
        ).order_by(desc(PostTable.createTime)).offset(page).limit(size).all()

        # 값을 반환: List<{postid, photoId, title, pHeart, comment, author_name, desc}>
        banners = []
        for i in post:
            # POST_CONTENT_DIR에 있는 파일 중 post_id경로의 content를 읽어온다.
            file_path = os.path.join(
                POST_CONTENT_DIR, str(i.post_id) + '.txt')
            with open(file_path, 'r', encoding='UTF-8') as f:
                content = f.read()

            # 위처럼 개행, 이미지 경로는 제거하고 100자로 자른다.
            content = re.sub(r'!\[\[(.*?)\]\]', '', content)
            content = re.sub(r'\n', '', content)
            if len(content) >= 100:
                descr = content[:100] + '...'
            else:
                descr = content

            # content에 ![[Image1.jpeg]] 형식의 이미지가 있으면 첫번째 이미지 경로를 가져온다.
            photoId = re.search(r'!\[\[(.*?)\]\]', content)
            if photoId:
                photoId = photoId.group(1)
            else:
                photoId = None

            banners.append({
                'post_id': i.post_id,
                'photoId': photoId,
                'title': i.title,
                'pHeart': i.pHeart,
                'comment': i.pComment,
                'author_name': db.query(ParentTable).filter(
                    ParentTable.parent_id == i.parent_id).first().name,
                'desc': descr
            })

        return banners

    def createPostMainHighView(self) -> CreatePostMainHighViewListOutput:
        """
        조회수가 높은 게시물
        --output
            - List<{postid, photoId, title, author_name, desc}> : 조회수가 높은 게시물
        """
        db = get_db_session()

        # 조회수가 높은 게시물을 가져옵니다.
        post = db.query(PostTable).order_by(
            desc(PostTable.pView)).limit(10).all()

        # 값을 반환: List<{postid, photoId, title, author_name, desc}>
        banners = []
        for i in post:
            # POST_CONTENT_DIR에 있는 파일 중 post_id경로의 content를 읽어온다.
            file_path = os.path.join(
                POST_CONTENT_DIR, str(i.post_id) + '.txt')
            with open(file_path, 'r', encoding='UTF-8') as f:
                content = f.read()

            photoId, descr = self._get_photoId_and_desc(content)

            banners.append({
                'post_id': i.post_id,
                'photoId': photoId,
                'title': i.title,
                'author_name': db.query(ParentTable).filter(
                    ParentTable.parent_id == i.parent_id).first().name,
                'desc': descr
            })

        return banners

    def createPostMainHashtag(self, parent_id: str) -> CreatePostMainHashtagListOutput:
        """
        많이 본 해시태그로 게시물 추천
        --input
            - parent_id: 부모 아이디
        --output
            - List<{postid, photoId, title, author_name, desc, hashList}> : 많이 본 해시태그로 게시물 추천
        """
        db = get_db_session()

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
            if post.hashList != None and post.hashList != '':
                post_hashlist = post.hashList.split(',')
                if any(hash in parent_hashlist for hash in post_hashlist):
                    matching_posts.append(post)
                if len(matching_posts) == 10:
                    break

        # 값을 반환: List<{postid, photoId, title, author_name, desc, hashList}>
        banners = []
        for i in matching_posts:
            # POST_CONTENT_DIR에 있는 파일 중 post_id경로의 content를 읽어온다.
            file_path = os.path.join(
                POST_CONTENT_DIR, str(i.post_id) + '.txt')
            with open(file_path, 'r', encoding='UTF-8') as f:
                content = f.read()

            photoId, descr = self._get_photoId_and_desc(content)

            banners.append({
                'post_id': i.post_id,
                'photoId': photoId,
                'title': i.title,
                'author_name': db.query(ParentTable).filter(
                    ParentTable.parent_id == i.parent_id).first().name,
                'desc': descr,
                'hash': i.hashList
            })
        return banners
