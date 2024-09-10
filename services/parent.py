from typing import Optional, Union, List
from fastapi import HTTPException, UploadFile
import bcrypt
import os
import shutil
from PIL import Image

from model.parent import ParentTable
from model.pbconnect import *
from constants.path import *

from schemas.parent import *

from db import get_db_session
from error.exception.customerror import *
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE


class ParentService:

    # 부모 생성
    def createParent(self, createParentInput: CreateParentInput):
        '''
        부모 생성
        --input
            - createParentInput.parent_id: 부모 아이디
            - createParentInput.email: 이메일
            - createParentInput.password: 비밀번호
            - createParentInput.nickname: 닉네임
            - createParentInput.signInMethod: 로그인 방식
            - createParentInput.emailVerified: 이메일 인증 여부
        --output
            - parent: 부모 정보
        '''
        db = get_db_session()

        # 부모 아이디 중복 확인
        error = db.query(ParentTable).filter(
            ParentTable.parent_id == createParentInput.parent_id).first()

        if error:
            raise CustomException("parent_id already exists")

        # 패스워드 암호화
        # if createParentInput.signInMethod == 'email':
        #     createParentInput.password = bcrypt.hashpw(
        #         createParentInput.password.encode('utf-8'), bcrypt.gensalt())

        # 이메일 중복 확인
        error = db.query(ParentTable).filter(
            ParentTable.email == createParentInput.email).first()

        if error:
            raise CustomException("email already exists")

        try:
            parent = ParentTable(
                parent_id=createParentInput.parent_id,
                password=createParentInput.password,
                email=createParentInput.email,
                name=None,
                nickname=createParentInput.nickname,
                gender=None,
                signInMethod=createParentInput.signInMethod,
                emailVerified=createParentInput.emailVerified,
                photoId=None,
                description=None,
                mainAddr=None,
                subAddr=None,
                hashList=None
            )

            db.add(parent)
            db.commit()
            db.refresh(parent)

            return parent

        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to create parent")

    # 부모 정보 조회
    def getParent(self, parent_id: str) -> Optional[Parent]:
        '''
        부모 정보 조회
        --input
            - parent_id: 부모 아이디
        --output
            - parent: 부모 정보
        '''
        db = get_db_session()

        parent = db.query(ParentTable).filter(
            ParentTable.parent_id == parent_id).first()

        return parent

    # 부모 정보 수정
    def updateParent(self, parent_id: str,
                     updateParentInput: UpdateParentInput) -> Optional[Parent]:
        '''
        부모 정보 수정
        --input\
            - parent_id: 부모 아이디
            - updateParentInput.password: 비밀번호
            - updateParentInput.email: 이메일
            - updateParentInput.name: 이름
            - updateParentInput.nickname: 닉네임
            - updateParentInput.gender: 성별 (0: 남성, 1: 여성, 2: 기타)
            - updateParentInput.signInMethod: 로그인 방식
            - updateParentInput.emailVerified: 이메일 인증 여부
            - updateParentInput.photoId: 사진 아이디
            - updateParentInput.description: 설명
            - updateParentInput.mainAddr: 주소
            - updateParentInput.subAddr: 상세 주소
            - updateParentInput.hashList: 해시 리스트
        --output
            - parent: 부모 정보
        '''

        db = get_db_session()
        try:
            parent = db.query(ParentTable).filter(
                ParentTable.parent_id == parent_id).first()

            if parent is None:
                return None

            # 패스워드 암호화
            if parent.signInMethod == 'email' and updateParentInput.password:
                updateParentInput.password = bcrypt.hashpw(
                    updateParentInput.password.encode('utf-8'), bcrypt.gensalt())

            for key in updateParentInput.dict().keys():
                value = updateParentInput.dict()[key]
                if value != None:
                    if key == 'password' and parent.signInMethod != 'email':
                        raise CustomException(
                            "signInMethod이 email이 아닌 경우 password를 수정할 수 없습니다.")
                    if key == 'photoId' and value == 'remove_photoId':
                        value = None
                    setattr(parent, key, value)

            db.add(parent)
            db.commit()
            db.refresh(parent)

            return parent

        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to update parent")

    def uploadProfileImage(self, file: UploadFile, parent_id: str) -> bool:
        """
        생성된 post에 대한 사진 업로드
        --input
            - file: 업로드할 파일 리스트
            - parent_id: 부모 아이디
        --output
            - bool: 사진 업로드 성공 여부
        """
        db = get_db_session()

        parent = db.query(ParentTable).filter(
            ParentTable.parent_id == parent_id).first()

        if parent is None:
            raise CustomException("Parent not found")

        # 파일 확장자를 file.filename에서 추출
        filename = file.filename
        if "." in filename:
            file_extension = filename.split(".")[-1].lower()
        else:
            raise CustomException("Invalid file format")

        # 이미지 파일 확장자만 허용 (jpg, jpeg, png, tiff, webp, heif, heic)
        allowed_extensions = ['jpg', 'jpeg',
                              'png', 'tiff', 'webp', 'heif', 'heic']
        if file_extension not in allowed_extensions:
            raise CustomException("이미지만 받을 수 있습니다.")

        # 파일 저장 경로 설정 (항상 .jpeg로 저장)
        file_path = os.path.join(PROFILE_IMAGE_DIR, f"{parent_id}.jpeg")

        # 파일을 jpeg로 변환 후 저장
        try:
            image = Image.open(file.file)
            rgb_image = image.convert("RGB")  # PNG, TIFF, HEIC 등은 RGB로 변환
            rgb_image.save(file_path, format="JPEG")
        except Exception as e:
            raise CustomException(f"이미지 처리 중 오류가 발생했습니다: {str(e)}")

        return True

    # 부모 삭제

    def deleteParent(self, parent_id: str) -> bool:
        '''
        부모 삭제
        --input
            - parent_id: 부모 아이디
        --output
            - bool 성공 여부
        '''
        db = get_db_session()
        try:
            parent = db.query(ParentTable).filter(
                ParentTable.parent_id == parent_id).first()

            if parent is None:
                return False

            db.delete(parent)
            db.commit()

            return True
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to delete parent")

    # 이메일리스트를 입력 받아 해당 부모의 특정 정보 가져오기
    def getFriends(self, emails: Optional[List[str]]) -> dict:
        '''
        이메일로 부모의 대략적인 정보 조회
        --input
            - emails: 이메일 (각 이메일을 ,로 구분하는 문자열)
        --output
            - friends_dict: 부모 정보
        '''
        db = get_db_session()
        friends_dict = {}
        try:
            if emails is not None:
                for email in emails:
                    parent = db.query(ParentTable).filter(
                        ParentTable.email == email).first()
                    if parent:
                        friends_dict[email] = {
                            'email': parent.email,
                            'name': parent.name,
                            'nickname': parent.nickname,
                            'description': parent.description
                        }
                return friends_dict

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to get friends")

    # def getParentAll(self):
    #     db=get_db_session()
    #     try:
    #         parent = db.query(ParentTable).all()

    #         return parent
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=400, detail="Failed to get parent")

    # 다른 아기-부모 연결 생성
    def create_pbconnect(self, baby_id: str, parent_id: str) -> Optional[PBConnect]:
        '''
        부모에게 다른 아기 연결 요청 (부부끼리 아기를 공유할 수 있음)
        --input
            - baby_id: 아기 아이디
            - parent_id: 부모 아이디
        --output
            - pbconnect: 부모-아기 연결 정보
        '''
        db = get_db_session()
        try:
            pbconnect = PBConnectTable(
                parent_id=parent_id,
                baby_id=baby_id
            )
            if pbconnect is None:
                return None

            db.add(pbconnect)
            db.commit()
            db.refresh(pbconnect)

            return pbconnect

        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to create pbconnect")

    # 부모 로그인
    def createLogin(self, createLoginInput: CreateLoginInput) -> Optional[Parent]:
        '''
        부모 로그인
        --input
            - createLoginInput.email: 이메일
            - createLoginInput.password: 비밀번호
        --output
            - parent: 부모 정보
        '''
        db = get_db_session()

        # 이메일이 존재하지 않으면 에러
        parent = db.query(ParentTable).filter(
            ParentTable.email == createLoginInput.email).first()

        if parent is None:
            raise CustomException("Email not found")

        # signInMethod가 'email'인 경우 비밀번호를 해싱해서 확인
        # if parent.signInMethod == 'email':
        #     # 입력된 비밀번호를 해싱
        #     if not bcrypt.checkpw(createLoginInput.password.encode('utf-8'), parent.password.encode('utf-8')):
        #         raise CustomException("wrong password")

        return parent
