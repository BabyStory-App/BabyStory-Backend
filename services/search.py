from fastapi import HTTPException
from typing import Optional, List
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from sqlalchemy import desc
from starlette.status import HTTP_400_BAD_REQUEST,HTTP_406_NOT_ACCEPTABLE

from model.post import PostTable
from model.parent import ParentTable

from schemas.search import *
from error.exception.customerror import *
from db import get_db_session

class SearchService:
    # 검색어 입력시 검색 결과 반환
    def createSearch(self, createSearchInput: CreateSearchInput) -> CreateSearchOutputListOutput:
        """
        검색어 입력시 검색 결과 반환하는 함수
        
        --input
            - search: 검색어
            - size: 검색 결과 개수
            - page: 페이지 수
        --output
            - List<{title, photoid,  author_name, heart, commnet, desc}>
        """
    
        db = get_db_session()
        try:
            if createSearchInput.size != -1 and createSearchInput.size <=0:
                raise CustomException("size must be -1 or greater than 0")
            if createSearchInput.page != -1 and createSearchInput.page <=0:
                raise CustomException("page must be -1 or greater than 0")
            
            # size와 page가 -1이면 기본 페이지를 가져온다.
            if createSearchInput.size == -1:
                size = 10
            else:
                size = createSearchInput.size
            
            if createSearchInput.page == -1:
                page = 1
            else:
                # 10개씩 보여주는 페이지일 경우 페이지의 시작점을 계산
                page = (createSearchInput.page - 1) * size + 1

            # 제목에 검색어가 포함된 게시물을 조회
            # .order_by(desc(PostTable.view)) 조회수는 포스트마다 계산하기 힘들어서 안함(post에 따로 저장하지않음)
            post = db.query(PostTable).filter(
                PostTable.title.ilike(f'%{createSearchInput.search}%')
            ).limit(size).offset(page).all()

            # 값을 반환: List<{title, photoid,  author_name, pHeart, pComment, desc}>
            banners = []
            for i in post:
                banners.append({
                    'title': i.title,
                    #'photo_id': i.photos,
                    'author_name': db.query(ParentTable).filter(
                        ParentTable.parent_id == i.parent_id).first().name,
                    'pHeart': i.pHeart,
                    'pComment': i.pComment
                    #,
                    #'desc': i.content[:100]
                })

            return banners
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="search not found")
        

