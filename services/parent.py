from typing import Optional, Union

from model.parent import Parent
from model.types.parent import ParentType
from schemas.parent import ParentCreateInput, ParentUpdateInput
from db import get_db_session


class ParentService:
    def __init__(self):
        self.model = Parent

    def create_parent(self, parent_input: ParentCreateInput) -> Union[ParentType, str]:
        db = get_db_session()
        try:
            # Check if email already exists
            if db.query(self.model).filter(self.model.email == parent_input.email).count() > 0:
                return "Email already exists"

            parent = self.model(
                uid=parent_input.uid,
                nickname=parent_input.nickname,
                email=parent_input.email,
            )
            db.add(parent)
            db.commit()
            db.refresh(parent)
            return ParentType(**parent.__dict__)
        except Exception as e:
            db.rollback()
            print(e)
            return "Failed to create parent"

    def get_parent(self, uid: str) -> Optional[ParentType]:
        db = get_db_session()
        print(f'uid: {uid}')
        try:
            # Get Parent from DB with primary key ui
            parent = db.query(self.model).filter(self.model.uid == uid).first()
            print(parent)
            print(uid)
            return ParentType(**parent.__dict__)
        except Exception as e:
            print(e)
            return None

    def update_parent(self, uid: str, parent_input: ParentUpdateInput) -> Union[ParentType, str]:
        db = get_db_session()
        try:
            parent = db.query(self.model).filter(
                self.model.uid == uid).first()
            if parent == None:
                return "Parent not found"

            if parent_input.email != None and parent.email != parent_input.email:
                if db.query(self.model).filter(self.model.email == parent_input.email).count() > 0:
                    return "Email already exists"
                parent.email = parent_input.email

            if parent_input.nickname != None:
                parent.nickname = parent_input.nickname
            if parent_input.photoId != None:
                parent.photoId = parent_input.photoId
            if parent_input.description != None:
                parent.description = parent_input.description

            db.commit()
            db.refresh(parent)
            return ParentType(**parent.__dict__)
        except Exception as e:
            db.rollback()
            return "Failed to update parent"

    def delete_parent(self, uid: str) -> bool:
        db = get_db_session()
        try:
            parent = db.query(self.model).filter(self.model.uid == uid).first()
            if parent == None:
                return True

            db.delete(parent)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            return False
