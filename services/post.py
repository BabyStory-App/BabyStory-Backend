from fastapi import HTTPException, UploadFile
from typing import Optional, List
from sqlalchemy.orm import joinedload
from constants.path import *

import os
import shutil
from uuid import uuid4
from schemas.post import *

from model.post import Post

from schemas.post import *

from db import get_db_session


class PostService:
    # 게시물 생성
    def createPost(self, parent_id: str,
<<<<<<< HEAD
                   createPostInput: CreatePostInput
                   #,file: UploadFile
                   ) -> Post:
        db = get_db_session()

        try:
            # save photo image if exists
            photo_id = None
            # if createPostInput.photoId != None:
            #     photo_id = str(uuid4())
            #     photo_save_path = os.path.join(
            #         PROJECT_DIR, f"{photo_id}.jpg")
            #     with open(photo_save_path, "wb") as buffer:
            #         shutil.copyfileobj(file.file, buffer)
=======
                   createPostInput: CreatePostInput) -> Post:
        
        """
        게시물 생성
        --input
            - createPostInput.reveal: 게시물 공개 여부
            - createPostInput.title: 게시물 제목
            - createPostInput.createTime: 게시물 생성 시간
            - createPostInput.pHeart: 게시물 하트 수
            - createPostInput.pScript: 게시물 스크립트
            - createPostInput.pView: 게시물 조회수
            - createPostInput.pComment: 게시물 댓글 수
            - createPostInput.hashList: 게시물 해시태그 리스트
        --output
            - Post: 게시물 딕셔너리
        """
                     
        db = get_db_session()

        try:
            if createPostInput.reveal not in [0, 1, 2, 3]:
                raise Exception("Invalid reveal value")
>>>>>>> a2e8541713403e69e360a6133b80d65e41d85440

            # print(createPostInput)
            post = PostTable(
                parent_id=parent_id,
                reveal=createPostInput.reveal,
                title=createPostInput.title,
                createTime=createPostInput.createTime,
                modifyTime=None,
                deleteTime=None,
                pHeart=createPostInput.pHeart,
                pScript=createPostInput.pScript,
                pView=createPostInput.pView,
                pComment=createPostInput.pComment,
                hashList=createPostInput.hashList if createPostInput.hashList else None
            )

            db.add(post)
            db.commit()
            db.refresh(post)

            # content를 txt 파일로 저장
            file_path = os.path.join(POST_CONTENT_DIR, str(post.post_id) + '.txt')
            with open(file_path, 'w', encoding='UTF-8') as f:
                f.write(createPostInput.content)

            return post
        
        except Exception as e:
            db.rollback()
            print(e)
            #raise Exception(e)
            raise Exception("Failed to create post")
        
    # 새로 생성된 post 사진 업로드
    def uploadPhoto(self, fileList: List[UploadFile], post_id: int, parent_id: str) -> bool:
        
        """
        새로 생성된 post 사진 업로드
        --input
            - fileList: 업로드할 파일 리스트
            - post_id: 게시물 아이디
            - parent_id: 부모 아이디
        --output
            - bool: 사진 업로드 성공 여부
        """
        
        db = get_db_session()

        try:
            post = db.query(PostTable).filter(
                PostTable.post_id == post_id, 
                PostTable.parent_id == parent_id,
                PostTable.deleteTime == None).first()
            
            if post is None:
                return False
            
            os.makedirs(os.path.join(POST_PHOTO_DIR, str(post.post_id)), exist_ok=True)
            
            # 사진 업로드
            for i, file in enumerate(fileList):
                file_type = file.content_type.split('/')[1]
                file_path = os.path.join(POST_PHOTO_DIR, str(post.post_id), f"{post.post_id}_{i + 1}.{file_type}")
                
                with open(file_path, 'wb') as f:
                    shutil.copyfileobj(file.file, f)
            
            return True
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to upload photo")
            return False
        
        

    # 모든 게시물 가져오기
    def getAllPost(self, parent_id: str) -> Optional[List[Post]]:

        """
        모든 게시물 가져오기
        --input
            - parent_id: 부모 아이디
        --output
            - List[Post]: 게시물 리스트
        """

        db = get_db_session()
        
        try:
            post = db.query(PostTable).filter(
                PostTable.parent_id == parent_id, 
                PostTable.deleteTime == None).all()

            if post is None:
                return None

            return post
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to get post")
        

    # 하나의 게시물 가져오기
    def getPost(self, post_id: str, parent_id: str) -> Optional[Post]:
        """
        하나의 게시물 가져오기
        --input
            - post_id: 게시물 아이디
            - parent_id: 부모 아이디
        --output
            - Post: 게시물 딕셔너리
        """
        db = get_db_session()

        try:
            post = db.query(PostTable).filter(
                PostTable.parent_id == parent_id,
                PostTable.post_id == post_id, 
                PostTable.deleteTime == None).first()

            if post is None:
                return None

            return post
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to get post")
        
    # 게시물 수정
    def updatePost(self, 
                   updatePostInput: UpdatePostInput, 
                   parent_id: str) -> Optional[Post]:
        
        """
        게시물 수정
        --input
            - updatePostInput.post_id: 게시물 아이디
            - updatePostInput.title: 게시물 제목
            - updatePostInput.post: 게시물 내용
            - updatePostInput.modify_time: 게시물 수정 시간
            - updatePostInput.hash: 게시물 해시태그 리스트
        --output
            - Post: 게시물 딕셔너리
        """
        db = get_db_session()

        try:
            post = db.query(PostTable).filter(
                PostTable.parent_id == parent_id,
                PostTable.post_id == updatePostInput.post_id,
                PostTable.deleteTime == None).first()
            
            if post is None:
                return None
            
            for key in ['title', 'post', 'modify_time', 'hash']:
                setattr(post, key, getattr(updatePostInput, key))

            db.add(post)
            db.commit()
            db.refresh(post)

            return post
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to update post")
        
    # 게시물 삭제
    def deletePost(self, 
                   deletePostInput: DeletePostInput, 
                   parent_id: str) -> Optional[Post]:
        """
        게시물 삭제
        --input
            - deletePostInput.post_id: 게시물 아이디
            - deletePostInput.deleteTime: 게시물 삭제 시간 datetime.now()
        --output
            - Post: 게시물 딕셔너리
        """
        db = get_db_session()

        try:
            post = db.query(PostTable).filter(
                PostTable.post_id == deletePostInput.post_id, 
                PostTable.parent_id == parent_id,
                PostTable.deleteTime == None).first()
            
            if post is None:
                return None
            
            setattr(post, 'deleteTime', deletePostInput.deleteTime)
            
            db.add(post)
            db.commit()
            db.refresh(post)
            
            return post
        
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to delete post")