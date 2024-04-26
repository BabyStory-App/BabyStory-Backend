from fastapi import HTTPException
from typing import Optional, List
from sqlalchemy.orm import joinedload

from model.post import Post

from schemas.post import *

from db import get_db_session

class PostService:

    # 게시물 생성
    def createPost(self, parent_id: str,
                   createPostInput: CreatePostInput) -> Post:
        db = get_db_session()
        try:
            print(createPostInput)
            post = PostTable(
                parent_id=parent_id,
                post=createPostInput.post,
                photos=createPostInput.photos if createPostInput.photos else None,
                post_time=createPostInput.post_time,
                modify_time=None,
                delete_time=None,
                heart=None,
                share=None,
                script=None,
                comment=None,
                hash=createPostInput.hash if createPostInput.hash else None
            )

            db.add(post)
            db.commit()
            db.refresh(post)

            return post
        
        except Exception as e:
            db.rollback()
            print(e)
            #raise Exception(e)
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
    def getPost(self, post_id: str, parent_id: str) -> Optional[Post]:
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
    def updatePost(self, 
                   updatePostInput: UpdatePostInput, 
                   parent_id: str) -> Optional[Post]:
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
        
    # 게시물 삭제
    def deletePost(self, 
                   deletePostInput: DeletePostInput, 
                   parent_id: str) -> Optional[Post]:
        db = get_db_session()

        try:
            post = db.query(PostTable).filter(
                PostTable.post_id == deletePostInput.post_id, 
                PostTable.parent_id == parent_id,
                PostTable.delete_time == None).first()
            
            if post is None:
                return None
            
            setattr(post, 'delete_time', deletePostInput.delete_time)
            
            db.add(post)
            db.commit()
            db.refresh(post)
            
            return post
        
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to delete post")