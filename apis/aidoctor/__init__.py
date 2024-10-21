from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE
from auth.auth_bearer import JWTBearer
from services.aidoctor import AiDoctorService

from error.exception.customerror import *
from constants.path import *
import os
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from core.env import env


router = APIRouter(
    prefix="/aidoctor",
    tags=["aidoctor"],
    responses={404: {"description": "Not found"}},
)


def create_vectordb():
    # 임베딩 모델 초기화
    embeddings_model = HuggingFaceEmbeddings(
        model_name='jhgan/ko-sbert-nli',
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    if not os.path.exists(f'{ASSET_DIR}/faiss_index'):
        file_path = os.path.join(AIDOCTOR_DIR, "data.csv")
        df = pd.read_csv(file_path, encoding='utf-8-sig')

        # Document 객체 생성 (메타데이터 포함)
        documents = [
            Document(
                page_content=row['질문'],
                metadata={'탭': row['탭'], '질문': row['질문'], '답변': row['답변']}
            ) for _, row in df.iterrows()
        ]

        # FAISS 벡터 저장소 생성
        vectorstore = FAISS.from_documents(documents,
                                           embedding=embeddings_model,
                                           distance_strategy=DistanceStrategy.COSINE)

        vectorstore.save_local(f'{ASSET_DIR}/faiss_index')

    else:
        vectorstore = FAISS.load_local(
            f'{ASSET_DIR}/faiss_index', embeddings=embeddings_model, allow_dangerous_deserialization=True)

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


@router.post("/{chatroom_id}")
async def new_ai_chat(region: str, chatroom_id: int, ask: str, parent_id: str = Depends(JWTBearer())):
    '''
    AI 의사와의 채팅방 생성
    - chatroom_id: 채팅방 아이디
    - ask: 질문
    - parent_id: 부모 아이디
    '''

    try:
        # 채팅방 유무 확인(존재하지 않을 경우 생성, 존재할 경우 가져오기)
        room_id = aiDoctorService.create_aichatroom(parent_id, chatroom_id)

        # RAG에서 k는 5로 설정되어 있음 수정 가능
        result = aiDoctorService.search_in_rag(
            vectorstore, ask, 5)

        # 프롬프트의 context 부분 생성
        llm_prompt = aiDoctorService.format_for_llm_prompt(result)

        # 이전 채팅 내역 가져오기
        previos_chat = aiDoctorService.load_chat_history(
            parent_id, chatroom_id)

        previos_prompt = "이전 채팅 내역:\n"

        # 이전 채팅 내역이 있을 경우 이전 채팅 내역을 추가하여 질문 생성
        if 'chat_history' in previos_chat:

            # 각 chat의 ask와 res를 가져와서 previos_prompt에 추가
            for chat in previos_chat["chat_history"]:
                previos_prompt += f"\n질문: {chat.ask}\n답변: {chat.res}\n"

            llm_prompt = previos_prompt + "\n" + llm_prompt

        response = aiDoctorService.ask_gpt(llm, llm_prompt, ask)

        # 채팅방에 채팅 추가
        chat = aiDoctorService.add_chat(
            parent_id, room_id, ask, response, region)

    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to create chatroom")

    return {"room_id": room_id,
            "llm_prompt": llm_prompt,
            "createTime": chat.createTime,
            "chat": chat
            }


@router.get("/mychatroom", dependencies=[Depends(JWTBearer())])
async def get_chatroom_list(parent_id: str = Depends(JWTBearer())):
    '''
    부모의 채팅방 리스트 가져오기
    - parent_id: 부모 아이디
    '''

    try:
        chatrooms = aiDoctorService.get_chatroom_list(parent_id)

    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get chatroom list")

    return {"status": 200 if chatrooms is not None else 404,
            "message": "Successfully get chatroom list" if chatrooms is not None else "Chatroom Not found",
            "chatrooms": chatrooms
            }


@router.get("/chatroom/{chatroom_id}", dependencies=[Depends(JWTBearer())])
async def load_chat_history(chatroom_id: int, parent_id: str = Depends(JWTBearer())):
    '''
    채팅방의 채팅 내역 가져오기
    - chatroom_id: 채팅방 아이디
    - parent_id: 부모 아이디
    '''

    try:
        if chatroom_id is None:
            raise CustomException("Invalid chatroom_id")

        result = aiDoctorService.load_chat_history(
            parent_id, chatroom_id)

    except CustomException as error:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE, detail=error.message)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Failed to get chat history")

    return {"room_id": chatroom_id,
            "createTime": result["roomCreateTime"],
            "chatList": result["chat_history"]
            }
