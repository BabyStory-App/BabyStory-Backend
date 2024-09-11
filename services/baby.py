from fastapi import UploadFile
from typing import Optional, List
from uuid import uuid4
from db import get_db_session
from error.exception.customerror import *
from constants.path import *
import os
from PIL import Image
from model.baby import Baby
from schemas.baby import *
from model.pbconnect import *


class BabyService:

    def createBaby(self, createBabyInput: CreateBabyInput) ->Baby:
        '''
        아기 생성
        --input
            - CreateBabyInput: 아기 정보
        --output
            - Baby: 아기 정보
        '''
        db = get_db_session()

        baby = BabyTable(
            baby_id=str(uuid4()),
            obn=createBabyInput.obn,
            name=createBabyInput.name,
            gender=createBabyInput.gender,
            birthDate=createBabyInput.birthDate,
            bloodType=createBabyInput.bloodType,
            cm=createBabyInput.cm,
            kg=createBabyInput.kg,
            photoId=createBabyInput.photoId if createBabyInput.photoId else None
        )
        db.add(baby)
        db.commit()
        db.refresh(baby)
        
        if baby is None:
            raise CustomException("baby is not created")

        return baby
    


    def createPbconnect(self, parent_id: str, baby_id: str) -> Optional[PBConnect]:
        '''
        아기-부모 관계 생성
        --input
            - parent_id: 부모 아이디
            - baby_id: 아기 아이디
        --output
            - PBConnect: 아기-부모 연결 정보
        '''
        db = get_db_session()

        pbconnect = PBConnectTable(
            parent_id=parent_id,
            baby_id=baby_id
        )
        db.add(pbconnect)
        db.commit()
        db.refresh(pbconnect)

        if pbconnect is None:
            raise CustomException("pbconnect is not created")

        return pbconnect
    


    def uploadProfileImage(self, file: UploadFile, baby_id: str, parent_id: str) -> bool:
        '''
        아기 사진 업로드
        --input
            - fileList: 업로드할 파일 리스트
            - baby_id: 아기 아이디
            - parent_id: 부모 아이디
        --output
            - uploadProfileImageOutput: 사진 업로드 성공 여부
        '''
        db = get_db_session()

        # 부모 아이디로 아기-부모 연결 정보 가져오기
        pbconnect = db.query(PBConnectTable).filter(
            PBConnectTable.parent_id == parent_id,
            PBConnectTable.baby_id == baby_id).first()
        if pbconnect is None:
            raise CustomException("pbconnect is not found")
        
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
        file_path = os.path.join(BABY_PROFILE_DIR, f"{parent_id}.jpeg")

        # 파일을 jpeg로 변환 후 저장
        try:
            image = Image.open(file.file)
            rgb_image = image.convert("RGB")  # PNG, TIFF, HEIC 등은 RGB로 변환
            rgb_image.save(file_path, format="JPEG")
        except Exception as e:
            raise CustomException(f"이미지 처리 중 오류가 발생했습니다: {str(e)}")
        
        return True



    def getBaby(self, parent_id: str) -> List[Baby]:
        '''
        아기 정보 가져오기
        --input
            - parent_id: 부모 아이디
        --output
            - List[Baby]: 아기 정보 리스트
        '''
        db = get_db_session()

        # 부모 아이디로 아기-부모 연결 정보 가져오기
        has = db.query(PBConnectTable).filter(PBConnectTable.parent_id == parent_id).all()

        # 부모 아이디에 연결된 모든 아기의 아이디를 가져옴
        baby_ids = [i.baby_id for i in has]

        # has에 해당하는 아기정보와 일치하는 아기정보를 가져옴
        baby = db.query(BabyTable).filter(BabyTable.baby_id.in_(baby_ids)).all()
        
        if baby is None:
            raise CustomException("baby is not found")

        return baby
            


    def updateBaby(self, updateBabyInput: UpdateBabyInput, parent_id: str) -> Optional[Baby]:
        '''
        아기 정보 수정
        --input
            - UpdateBabyInput: 수정할 아기 정보
            - parent_id: 부모 아이디
        --output
            - Baby: 수정된 아기 정보
        '''
        db = get_db_session()

        # 다른 사람의 아기를 수정하는 것을 방지하기 위해 부모의 아기인지 확인해야함
        pbconnect = db.query(PBConnectTable).filter(
            PBConnectTable.parent_id == parent_id,
            PBConnectTable.baby_id == updateBabyInput.baby_id).first()
        if pbconnect is None:
            raise CustomException("pbconnect is not found")
        
        # 아기 정보
        baby = db.query(BabyTable).filter(
            BabyTable.baby_id == updateBabyInput.baby_id).first()
        if baby is None:
            raise CustomException("baby is not found")
        
        # 아기 정보 수정
        for key in ['obn', 'name', 'gender', 'birthDate', 'bloodType', 'photoId']:
            setattr(baby, key, getattr(updateBabyInput, key))
        db.add(baby)
        db.commit()
        db.refresh(baby)

        return baby
        


    def deleteBaby(self, baby_id: str,
                    parent_id: str) -> bool:
        '''
        아기 삭제
        --input
            - baby_id: 아기 아이디
            - parent_id: 부모 아이디
        --output
            - bool: 삭제 성공 여부
        '''
        db = get_db_session()

        # 다른 사람의 아기를 삭제하는 것을 방지하기 위해 부모의 아기인지 확인해야함
        pbconnect = db.query(PBConnectTable).filter(
            PBConnectTable.parent_id == parent_id,
            PBConnectTable.baby_id == baby_id).first()
        db.delete(pbconnect)
        db.commit()

        if pbconnect is None:
            raise CustomException("pbconnect is not found")

        # 아기 삭제
        baby = db.query(BabyTable).filter(
            BabyTable.baby_id == baby_id).first()
        if baby == None:
            raise CustomException("baby is not found")

        db.delete(baby)
        db.commit()

        return True