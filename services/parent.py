from typing import Optional, Union
from fastapi import HTTPException

from model.parent import ParentTable
from model.pbconnect import *

from schemas.parent import *

from db import get_db_session


class ParentService:

    # 부모 생성
    def createParent(self, createParentInput: CreateParentInput) :
        db = get_db_session()
        print(createParentInput)
        try:
            parent = ParentTable(
                parent_id=createParentInput.parent_id,
                password=createParentInput.password,
                email=createParentInput.email,
                name=createParentInput.name,
                nickname=createParentInput.nickname,
                gender=createParentInput.gender,
                signInMethod=createParentInput.signInMethod,
                emailVerified=createParentInput.emailVerified,
                photoId=createParentInput.photoId if createParentInput.photoId else None,
                description=createParentInput.description if createParentInput.description else None,
                mainAddr=createParentInput.mainAddr if createParentInput.mainAddr else None,
                subAddr=createParentInput.subAddr if createParentInput.subAddr else None,
                hashList=createParentInput.hashList if createParentInput.hashList else None
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
    def getParentByEmail(self, parent_id: str) -> Optional[Parent]:
        db = get_db_session()
        try:
            parent = db.query(ParentTable).filter(
                ParentTable.parent_id == parent_id).first()

            return parent
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to get parent")

    # 부모 정보 수정
    def updateParent(self, parent_id: str, 
                     updateParentInput: UpdateParentInput) -> Optional[Parent]:
        db = get_db_session()
        try:
            parent = db.query(ParentTable).filter(
                ParentTable.parent_id == parent_id).first()
            
            if parent is None:
                return False

            for key in updateParentInput.dict().keys():
                setattr(parent, key, updateParentInput.dict()[key])

            db.add(parent)
            db.commit()
            db.refresh(parent)

            return parent
        
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=400, detail="Failed to update parent")
        

    # 부모 삭제
    def deleteParent(self, parent_id: str) -> bool:
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
    def getFriends(self, emails: Optional[str]) -> GetFriendsByEmailOutput:
        db = get_db_session()
        friends_dict = {}
        try:
            if emails:
                for email in emails:
                    parent = db.query(ParentTable.email, ParentTable.name, ParentTable.nickname, ParentTable.description) \
                        .filter(ParentTable.email == email) \
                        .first()
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
    def create_pbconnect(self,  baby_id: str,parent_id: str) -> Optional[PBConnect]:
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
