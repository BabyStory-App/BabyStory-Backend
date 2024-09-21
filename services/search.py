from fastapi import HTTPException
from typing import Optional, List
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from sqlalchemy import desc
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from constants.path import *
import os
import re

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
        if createSearchInput.size != -1 and createSearchInput.size < 0:
            raise CustomException("size must be -1 or greater than 0")
        if createSearchInput.page != -1 and createSearchInput.page < 0:
            raise CustomException("page must be -1 or greater than 0")

            # size와 page가 -1이면 기본 페이지를 가져온다.
        if createSearchInput.size == -1 or createSearchInput.size == 0:
            size = 10
        else:
            size = createSearchInput.size

        if createSearchInput.page == -1 or createSearchInput.page == 0:
            page = 0
        else:
            # 10개씩 보여주는 페이지일 경우 페이지의 시작점을 계산
            page = createSearchInput.page * size

            # 제목에 검색어가 포함된 게시물을 조회
            # 조회수가 높은 순으로 정렬
        post = db.query(PostTable).filter(
            PostTable.title.ilike(f'%{createSearchInput.search}%')
        ).order_by(desc(PostTable.pView)).offset(page).limit(size).all()

        # 값을 반환: List<{title, photoid,  author_name, pHeart, pComment, desc}>
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
                'title': i.title,
                'photo_id': photoId,
                'author_name': db.query(ParentTable).filter(
                    ParentTable.parent_id == i.parent_id).first().name,
                'pHeart': i.pHeart,
                'pComment': i.pComment,
                'desc': descr
            })

        return banners
