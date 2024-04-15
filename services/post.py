from fastapi import HTTPException
from typing import Optional, List
from sqlalchemy.orm import joinedload

from model.post import Post

from schemas.post import *

from db import get_db_session

class PostService:

    # 게시물 생성
    def createPost(self,
                   createPostInput: CreatePostInput) -> Post:
        db = get_db_session()

        try:
            post = PostTable(
                post_id=createPostInput.post_id,
                post=createPostInput.post,
                photos=createPostInput.photos if createPostInput.photos else None,
                post_time=createPostInput.post_time,
                modify_time=createPostInput.modify_time if createPostInput.modify_time else None,
                delete_time=createPostInput.delete_time if createPostInput.delete_time else None,
                heart=createPostInput.heart if createPostInput.heart else None,
                share=createPostInput.share if createPostInput.share else None,
                script=createPostInput.script if createPostInput.script else None,
                comment=createPostInput.comment if createPostInput.comment else None,
                hash=createPostInput.hash if createPostInput.hash else None
            )

            db.add(post)
            db.commit()
            db.refresh(post)

            return post
        
        except Exception as e:
            db.rollback()
            print(e)
            raise Exception("Failed to create post")
        

    # 모든 게시물 가져오기
    def getAllPost(self, parent_id: str) -> Optional[List[Post]]:
        db = get_db_session()
        try:
            post = db.query(PostTable).filter(
                PostTable.parent_id == parent_id, 
                PostTable.delete_time == None).all()

            if post is None:
                return None

            return post
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to get post")
        

    # 하나의 게시물 가져오기
    def getPost(self, post_id: str, parent_id: str) -> Post:
        db = get_db_session()
        try:
            post = db.query(PostTable).filter(
                PostTable.parent_id == parent_id,
                PostTable.post_id == post_id, 
                PostTable.delete_time == None).first()

            if post is None:
                return None

            return post
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to get post")
        
    # 게시물 수정
    def updatePost(self, updatePostInput: UpdatePostInput, parent_id: str) -> Optional[Post]:
        db = get_db_session()

        try:
            post = db.query(PostTable).filter(
                PostTable.parent_id == parent_id,
                PostTable.post_id == updatePostInput.post_id, 
                PostTable.delete_time == None).first()
            
            if post is None:
                return None
            
            for key in ['post', 'photos', 'modify_time', 'hash']:
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