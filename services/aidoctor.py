from fastapi import HTTPException
from typing import Optional, List, Set
from db import get_db_session
from datetime import datetime

from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
import os
import json
import urllib.request
import requests

from model.aidoctorroom import AIDoctorRoomTable, AIDoctorRoom
from model.aidoctorchat import AIDoctorChatTable, AIDoctorChat
from schemas.aidoctor import *
from error.exception.customerror import *


class AiDoctorService:
    # RAG 검색
    def search_in_rag(self, vectorstore, query: str, k: int):
        """
        query를 RAG로 검색하여 답변을 얻는 함수
        --input
            - query: 질문
            - k: RAG로부터 나올 output 개수
            - parent_id: 부모 id
        --output
            - 답변 리스트
                - 탭: 탭 이름
                - 질문: 질문 내용
                - 답변: 답변 내용
        """

        retriever = vectorstore.as_retriever(
            search_type='mmr',
            search_kwargs={'k': k, 'lambda_mult': 0.9}
        )

        results = retriever.get_relevant_documents(query)

        return [
            {
                '탭': doc.metadata['탭'],
                '질문': doc.metadata['질문'],
                '답변': doc.metadata['답변']
            } for doc in results
        ]

    def format_for_llm_prompt(self, results):
        """
        RAG 결과를 통해 프롬프트의 context 부분을 얻는 함수
        --input
            - results: RAG 결과
        --output
            - 프롬프트의 context 부분
        """
        prompt = "다음은 검색된 유사한 질문과 답변입니다:\n\n"

        try:
            for idx, result in enumerate(results, 1):
                prompt += f"질문 {idx}: {result['질문']}\n"
                prompt += f"답변 {idx}: {result['답변']}\n"
                prompt += f"{result['탭']})\n\n"
        except KeyError as e:
            raise KeyError(f"결과 딕셔너리에 필요한 키가 없습니다: {e}")
        except Exception as e:
            raise Exception(f"프롬프트 생성 중 오류 발생: {e}")

        return prompt

    def ask_gpt(self, llm, llm_prompt, query):
        """
        RAG 결과를 GPT에 넣어 답변을 얻는 함수
        --input
            - llm: GPT 모델
            - llm_prompt: RAG 결과
        --output
            - 답변 리스트
        """

        template = """
        {context}
        위의 정보를 참고하여 질환에 대해서 자세히 설명하고 다음 질문에 답해주세요:
        질문: {question}
        (한국어로 답변, 병원 추천이 필요하다면 "더 정확한 진단과 치료가 필요하시면 가까운 ?를 방문하는 것이 좋습니다." 라고 뒤에 말해줘)답변:"""

        # 질문 포맷 생성
        prompt = ChatPromptTemplate.from_template(template)

        # Chain: 질문 포맷 -> OpenAI 모델 -> 답변 출력 파이프라인 정의
        chain = prompt | llm | StrOutputParser()

        response = chain.invoke({'context': (llm_prompt), 'question': query})

        return response

    def create_aichatroom(self, parent_id: str, room_id: Optional[int]) -> int:
        """
        AI 의사 채팅방 생성
        --input
            - parent_id: 부모 아이디
            - room_id: 채팅방 아이디
        --output
            - 생성된 채팅방 정보
        """

        db = get_db_session()

        # room_id로 채팅방 정보 조회
        room = db.query(AIDoctorRoomTable).filter(
            AIDoctorRoomTable.id == room_id).first()

        if room is None:
            try:
                # 채팅방 생성
                room = AIDoctorRoomTable(
                    parent_id=parent_id,
                    createTime=datetime.now()
                )

                db.add(room)
                db.commit()
                db.refresh(room)

            except Exception as e:
                db.rollback()
                raise CustomException("Failed to create chatroom")

            return room.id

        else:
            # room_id가 parent_id의 채팅방인지 확인
            if db.query(AIDoctorRoomTable).filter(room.id == room_id, room.parent_id == parent_id).first() is None:
                raise CustomException("Not your chatroom")

            return room.id

    def kakao_api_request(self, region: str, query: str) -> dict:
        """
        카카오 API를 통해 병원 정보를 가져오는 함수
        --input
            - region: 지역
            - query: 검색어
        --output
            - 병원 정보
        """

        kakao_api_key = os.getenv("KAKAO_REST_API_KEY")
        query = region + " " + query
        encText = urllib.parse.quote(query)

        url = "https://dapi.kakao.com/v2/local/search/keyword.json?query=" + encText + "&size=1"
        # &x=127.423084&y=37.078956&radius=20000 x경도 y위도 radius반경m단위
        headers = {
            "Authorization": "KakaoAK " + kakao_api_key
        }

        response = requests.get(url, headers=headers).json()['documents']

        if response is not None:

            return response
        else:
            raise CustomException("Failed to request kakao api")

    def add_chat(self, parent_id: str, room_id: int, ask: str, res: str, region: str) -> AIDoctorChat:
        """
        AI 의사 채팅방에 질문,답변 추가
        --input
            - parent_id: 부모 아이디
            - room_id: 채팅방 아이디
            - ask: 질문
            - res: 답변
            - region: 지역
        --output
            - 추가된 질문 정보
        """

        db = get_db_session()

        # res에서 병원 추천 정보 추출
        hospital = None
        # region = "강남대학교"

        if "더 정확한 진단과 치료가 필요하시면 가까운" in res:
            hospital = res.split("더 정확한 진단과 치료가 필요하시면 가까운")[
                1].split("를")[0].split("을")[0]

            hospital = self.kakao_api_request(region, hospital)
            hospital = hospital[0]

        try:
            # 질문 추가
            chat = AIDoctorChatTable(
                parent_id=parent_id,
                room_id=room_id,
                createTime=datetime.now(),
                ask=ask,
                res=res,
                hospital=hospital
            )

            db.add(chat)
            db.commit()
            db.refresh(chat)

        except Exception as e:
            db.rollback()
            raise CustomException("Failed to add chat")

        return chat

    def get_chatroom_list(self, parent_id: str) -> List[AIDoctorRoom]:
        """
        AI 의사 채팅방 리스트 조회
        --input
            - parent_id: 부모 아이디
        --output
            - 채팅방 리스트
        """

        db = get_db_session()

        # 부모 아이디로 채팅방 리스트 조회
        chatrooms = db.query(AIDoctorRoomTable).filter(
            AIDoctorRoomTable.parent_id == parent_id).order_by(AIDoctorRoomTable.createTime.desc()).all()

        # 각 채팅방의 마지막 채팅 정보인 res의 초반 100자, id, createTime을 lastChat 딕셔너리로 추가
        for room in chatrooms:
            lastChat = db.query(AIDoctorChatTable).filter(
                AIDoctorChatTable.room_id == room.id).order_by(AIDoctorChatTable.createTime.desc()).first()
            if lastChat is not None:
                room.lastChat = {
                    "id": lastChat.id,
                    "createTime": lastChat.createTime,
                    "res": lastChat.res[:100]
                }

        return chatrooms

    def load_chat_history(self, parent_id: str, chatroom_id: int) -> Optional[LoadChatHistoryServiceOutput]:
        """
        채팅방의 채팅 내역 조회
        --input
            - parent_id: 부모 아이디
            - chatroom_id: 채팅방 아이디
        --output
            - 채팅 내역 리스트
        """

        db = get_db_session()

        result = None

        # chatroom_id로 채팅방이 존재하는지 확인
        if db.query(AIDoctorRoomTable).filter(AIDoctorRoomTable.id == chatroom_id
                                              ).first() is not None:

            # parent_id와 chatroom_id의 parent_id가 일치하는지 확인
            if db.query(AIDoctorRoomTable).filter(
                    AIDoctorRoomTable.id == chatroom_id, AIDoctorRoomTable.parent_id == parent_id).first() is None:
                raise CustomException("Not your chatroom")

            # 채팅방 아이디로 채팅 내역 조회
            chat_history = db.query(AIDoctorChatTable).filter(
                AIDoctorChatTable.room_id == chatroom_id).order_by(AIDoctorChatTable.createTime.asc()).all()

            roomCreateTime = db.query(AIDoctorRoomTable).filter(
                AIDoctorRoomTable.id == chatroom_id).first().createTime

            result = {"roomCreateTime": roomCreateTime,
                      "chat_history": chat_history}

        return result
