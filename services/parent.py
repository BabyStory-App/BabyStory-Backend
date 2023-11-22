from typing import Optional

from model.parent import Parent
from schemas.parent import ParentCreateInput
from db import get_db_session
from schemas.parent import ParentType


class ParentService:
    def __init__(self):
        self.model = Parent

    def create_parent(self, parent_input: ParentCreateInput) -> Optional[ParentType]:
        db = get_db_session()
        try:
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
            return None

    def get_parent(self, uid: str) -> Optional[ParentType]:
        db = get_db_session()
        try:
            # Get Parent from DB with primary key ui
            parent = db.query(self.model).filter(self.model.uid == uid).first()
            return ParentType(**parent.__dict__)
        except Exception as e:
            return None
