from fastapi import HTTPException, UploadFile
from typing import Optional, List
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from constants.path import *
import os
import re
import shutil
from uuid import uuid4
from datetime import datetime
import random

from schemas.post import *
from model.post import Post
from schemas.post import *
from db import get_db_session
from error.exception.customerror import *
from model.friend import FriendTable


class PostService:

    # 부모의 상태 가져오기
    def _getParentStatus(self, parent_id: str):
        db = get_db_session()

        # 내가 친구로 등록한 부모 수
        friendCount = db.query(FriendTable).filter(
            FriendTable.parent_id == parent_id).count()

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


    # 게시물 생성
    def createPost(self, parent_id: str, createPostInput: CreatePostInput) -> Post:
        """
        게시물 생성
        - input
            - parent_id (str): 부모 아이디
            - createPostInput (CreatePostInput): 게시물 생성 정보
        - output
            - post (Post): 게시물 딕셔너리 
        """
        db = get_db_session()

        # 공개 범위 ( 0 ~ 3 ) 안의 값이 들어왔는지 확인합니다.
        if createPostInput.reveal not in [0, 1, 2, 3]:
            raise CustomException("Invalid reveal value")

        # print(createPostInput)
        post = PostTable(
            parent_id=parent_id,
            reveal=createPostInput.reveal,
            title=createPostInput.title,
            createTime=datetime.now(),
            modifyTime=None,
            deleteTime=None,
            pHeart=0,
            pScript=0,
            pView=0,
            pComment=0,
            hashList=createPostInput.hashList if createPostInput.hashList else None
        )

        db.add(post)
        db.commit()
        db.refresh(post)

        # content 파일의 tempPostId를 post_id로 변경
        content = createPostInput.content.replace(
            '![[tempPostId', f'![[{post.post_id}')

        # content를 txt 파일로 저장
        file_path = os.path.join(POST_CONTENT_DIR, str(post.post_id) + '.txt')
        with open(file_path, 'w', encoding='UTF-8') as f:
            f.write(content)

        return post


    # 새로 생성된 post 사진 업로드
    def uploadPhoto(self, fileList: List[UploadFile], post_id: int, parent_id: str) -> bool:
        """
        생성된 post에 대한 사진 업로드
        --input
            - fileList: 업로드할 파일 리스트
            - post_id: 게시물 아이디
            - parent_id: 부모 아이디
        --output
            - bool: 사진 업로드 성공 여부
        """
        db = get_db_session()

        post = db.query(PostTable).filter(
            PostTable.post_id == post_id,
            PostTable.parent_id == parent_id,
            PostTable.deleteTime == None).first()

        # post가 없을 경우 CustomException을 발생시킵니다.
        if post is None:
            raise CustomException("Post not found")

        # post 사진에 대한 디렉토리를 생성합니다.
        os.makedirs(os.path.join(POST_PHOTO_DIR,
                    str(post.post_id)), exist_ok=True)

        # 생성된 디렉토리에 사진을 저장합니다.
        for i, file in enumerate(fileList):
            file_type = file.content_type.split('/')[1]
            file_path = os.path.join(POST_PHOTO_DIR, str(
                post.post_id), f"{post.post_id}-{i + 1}.{file_type}")

            with open(file_path, 'wb') as f:
                shutil.copyfileobj(file.file, f)

        return True


    # 모든 게시물 가져오기
    async def getAllPost(self) -> Optional[List[Post]]:
        """
        모든 게시물 가져오기
        --input
            - parent_id: 부모 아이디
        --output
            - List[Post]: 게시물 리스트
        """
        db = get_db_session()

        post = db.query(PostTable).filter(
            PostTable.deleteTime == None).all()

        random.shuffle(post)

        return post

    def _get_photoId_and_desc(self, content: str):
        # content에 ![[Image1.jpeg]] 형식의 이미지가 있으면 첫번째 이미지 경로를 가져온다.
        photoIdRex = re.search(r'!\[\[(.*?)\]\]', content)
        photoId = photoIdRex.group(1) if photoIdRex else None

        # 위처럼 개행, 이미지 경로는 제거하고 100자로 자른다.
        content = re.sub(r'!\[\[(.*?)\]\]', '', content)
        descr = content if len(
            content) < 100 else content[:100] + '...'

        return photoId, descr


    # 특정 부모의 모든 게시물 가져오기
    async def getAllPostByParent(self, parent_id: str, limit: Optional[int]):
        """
        특정 부모의 모든 게시물 가져오기
        --input
            - parent_id: 부모 아이디
            - limit: 가져올 게시물 수
        --output
            - List[Post]: 게시물 리스트
        """
        db = get_db_session()
        _data = db.query(PostTable).where(
            PostTable.parent_id == parent_id).all()
        posts = random.sample(_data, len(
            _data) if len(_data) < limit else limit) if limit else _data
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
                'pView': i.pView,
                'pScript': i.pScript,
                'pHeart': i.pHeart,
                'comment': i.pComment,
                'author_name': db.query(ParentTable).filter(ParentTable.parent_id == i.parent_id).first().name,
                'desc': descr
            })
        return banners


    # 하나의 게시물 가져오기
    async def getPost(self, post_id: str):
        """
        하나의 게시물 가져오기
        --input
            - post_id: 게시물 아이디
        --output
            - Post: 게시물 딕셔너리
        """
        db = get_db_session()

        post = db.query(PostTable).filter(
            PostTable.post_id == post_id,
            PostTable.deleteTime == None).first()

        # post가 없을 경우 CustomException을 발생시킵니다.
        if post is None:
            raise CustomException("Post not found")

        creater = db.query(ParentTable).filter(
            ParentTable.parent_id == post.parent_id).first()
        status = self._getParentStatus(post.parent_id)
        post.__setattr__('creater', {
            "parentId": creater.parent_id,
            "email": creater.email,
            "name": creater.name,
            "nickname": creater.nickname,
            "photoId": creater.photoId,
            "description": creater.description,
            "status": status,
        })
        postContent = open(os.path.join(POST_CONTENT_DIR, str(
            post.post_id) + '.txt'), 'r', encoding='UTF-8').read()
        post.__setattr__('content', postContent)

        match = re.search(r'!\[\[(.*?)\]\]', postContent)
        post.__setattr__('photoId', match.group(1) if match else None)

        return post


    # 게시물 수정
    async def updatePost(self, updatePostInput: UpdatePostInput, parent_id: str) -> Optional[Post]:
        """
        게시물 수정
        --input
            - updatePostInput.post_id: 게시물 아이디
            - updatePostInput.title: 게시물 제목
            - updatePostInput.content: 게시물 내용
            - updatePostInput.modifyTime: 게시물 수정 시간
            - updatePostInput.hashList: 게시물 해시태그 리스트
        --output
            - Post: 게시물 딕셔너리
        """
        db = get_db_session()

        # 공개 범위 ( 0 ~ 3 ) 안의 값이 들어왔는지 확인합니다.
        if updatePostInput.reveal not in [0, 1, 2, 3]:
            raise CustomException("Invalid reveal value")

        post = db.query(PostTable).filter(
            PostTable.parent_id == parent_id,
            PostTable.post_id == updatePostInput.post_id,
            PostTable.deleteTime == None).first()

        # # post가 없을 경우 CustomException을 발생시킵니다.
        # if post is None:
        #     raise CustomException("Post not found")

        for key in ['reveal', 'title', 'hashList']:
            setattr(post, key, getattr(updatePostInput, key))
        setattr(post, 'modifyTime', datetime.now())

        # content를 기존에 존재하는 txt 파일에 덮어씌웁니다.
        file_path = os.path.join(POST_CONTENT_DIR, str(post.post_id) + '.txt')
        with open(file_path, 'w', encoding='UTF-8') as f:
            f.write(updatePostInput.content)

        db.add(post)
        db.commit()
        db.refresh(post)

        return post


    # 게시물 삭제
    async def deletePost(self, deletePostInput: DeletePostInput, parent_id: str) -> Optional[Post]:
        """
        게시물 삭제
        --input
            - deletePostInput.post_id: 게시물 아이디
            - deletePostInput.deleteTime: 게시물 삭제 시간 datetime.now()
        --output
            - Post: 게시물 딕셔너리
        """
        db = get_db_session()

        post = db.query(PostTable).filter(
            PostTable.post_id == deletePostInput.post_id,
            PostTable.parent_id == parent_id,
            PostTable.deleteTime == None).first()

        # post가 없을 경우 CustomException을 발생시킵니다.
        if post is None:
            raise CustomException("Post not found")

        # post의 data를 삭제하지 않고 deleteTime을 추가하여 삭제된 것으로 표시합니다.
        setattr(post, 'deleteTime', datetime.now())

        db.add(post)
        db.commit()
        db.refresh(post)

        return post
