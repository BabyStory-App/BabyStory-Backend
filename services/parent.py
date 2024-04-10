from typing import Optional, Union
from fastapi import APIRouter, FastAPI

from model.parent import ParentTable
from model.parent import Parent

from schemas.parent import *
from db import get_db_session


class ParentService:

    def createParent(self, i: CreateParentInput) -> CreateParentOutput:
        db = get_db_session()
        try:
            parent = ParentTable(
                parent_id=i.parent_id,
                password=i.password,
                email=i.email,
                name=i.name,
                nickname=i.nickname,
                signInMethod=i.signInMethod,
                emailVerified=i.emailVerified,
                photoId=i.photoId,
                description=i.description
            )
            db.add(parent)
            db.commit()
            db.refresh(parent)

            return parent

        except Exception as e:
            db.rollback()
            raise Exception(e)

    def getParentByEmail(self, id: str) -> GetParentByEmailOutput:
        db = get_db_session()
        try:
            parent = db.query(ParentTable).filter(
                ParentTable.parent_id == id).first()

            return parent
        except Exception as e:
            raise Exception(e)

    def updateParent(self, uid: str, p: UpdateParentInput) -> bool:
        db = get_db_session()
        try:
            parent = db.query(ParentTable).filter(
                ParentTable.parent_id == uid).first()
            if parent is None:
                return False

            setattr(parent, "password", parent.password)
            setattr(parent, "email", parent.email)
            setattr(parent, "name", parent.name)
            setattr(parent, "nickname", parent.nickname)
            setattr(parent, "signInMethod", parent.signInMethod)
            setattr(parent, "emailVerified", parent.emailVerified)
            setattr(parent, "photoId", parent.photoId)
            setattr(parent, "description", parent.description)

            db.add(parent)
            db.commit()
            db.refresh(parent)

            return True
        except Exception as e:
            db.rollback()
            raise Exception(e)

    def deleteParent(self, uid: str) -> bool:
        db = get_db_session()
        try:
            parent = db.query(ParentTable).filter(
                ParentTable.parent_id == uid).first()
            if parent is None:
                return False

            db.delete(parent)
            db.commit()

            return True
        except Exception as e:
            db.rollback()
            raise Exception(e)

    def getFriends(self, emails: Optional[str]) -> GetFriendsByEmailOuput:
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
            raise Exception(e)

    # def getParentAll(self):
    #     db=get_db_session()
    #     try:
    #         parent = db.query(ParentTable).all()

    #         return parent
    #     except Exception as e:
    #         raise Exception(e)
