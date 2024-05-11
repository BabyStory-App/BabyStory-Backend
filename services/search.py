from fastapi import HTTPException
from typing import Optional, List
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from sqlalchemy import desc

from model.post import PostTable
from model.parent import ParentTable

from schemas.search import *
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
        # 10개씩 보여주는 페이지일 경우 페이지의 시작점을 계산
        page = ( createSearchInput.page - 1 ) * 10

        db = get_db_session()
        try:
            # 제목에 검색어가 포함된 게시물을 조회
            # .order_by(desc(PostTable.view)) 조회수는 포스트마다 계산하기 힘들어서 안함(post에 따로 저장하지않음)
            post = db.query(PostTable).filter(
                PostTable.post.like(f'%{createSearchInput.search}%')
            ).limit(createSearchInput.size).offset(page).all()

            # 값을 반환: List<{title, photoid,  author_name, heart, commnet, desc}>
            banners = []
            for i in post:
                banners.append({
                    'title': i.title,
                    'photo_id': i.photos,
                    'author_name': db.query(ParentTable).filter(
                        ParentTable.parent_id == i.parent_id).first().name,
                    'heart': i.heart,
                    'comment': i.comment,
                    'desc': i.post[:100]
                })

            return banners
        
        except Exception as e:
            #raise (e)
            raise HTTPException(status_code=400, detail="search not found")
        

