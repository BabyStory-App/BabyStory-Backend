from fastapi import APIRouter, HTTPException, UploadFile, Depends, Form
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer
from services.aidoctor import AiDoctorService
# from schemas.baby import *
from error.exception.customerror import *
from constants.path import *
import os
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.vectorstores.utils import DistanceStrategy
from core.env import env

router = APIRouter(
    prefix="/aidoctor",
    tags=["aidoctor"],
    responses={404: {"description": "Not found"}},
)


def create_vectordb():
    file_path = os.path.join(AIDOCTOR_DIR, "data.csv")
    df = pd.read_csv(file_path, encoding='utf-8-sig')

    # Document 객체 생성 (메타데이터 포함)
    documents = [
        Document(
            page_content=row['질문'],
            metadata={'탭': row['탭'], '질문': row['질문'], '답변': row['답변']}
        ) for _, row in df.iterrows()
    ]

    # 임베딩 모델 초기화
    embeddings_model = HuggingFaceEmbeddings(
        model_name='jhgan/ko-sbert-nli',
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    # FAISS 벡터 저장소 생성
    vectorstore = FAISS.from_documents(documents,
                                       embedding=embeddings_model,
                                       distance_strategy=DistanceStrategy.COSINE)

    return vectorstore


vectorstore = create_vectordb()
llm = ChatOpenAI(
    model='gpt-3.5-turbo-0125',
    temperature=0,
    max_tokens=500,
    openai_api_key=env.get("OPEN_API_KEY")
)
aiDoctorService = AiDoctorService()


@router.post("/create")
async def aidoc(query: str, k: int):
    '''
    AI 의사의 답변을 얻기 위한 API
    - query: 질문
    - k: RAG로부터 나올 output 개수
    '''

    try:
        # RAG 생성
        result = aiDoctorService.search_in_rag(
            vectorstore, query, k)

        # 프롬프트의 context 부분 생성
        llm_prompt = aiDoctorService.format_for_llm_prompt(result)

        response = aiDoctorService.ask_gpt(llm, llm_prompt, query)

    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get response aidoctor")

    return {'aidoctor': response}
