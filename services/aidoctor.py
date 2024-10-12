from fastapi import HTTPException
from typing import Optional, List, Set
from db import get_db_session

from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate

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
