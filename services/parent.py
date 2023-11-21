from model.parent import Parent
from schemas.parent import ParentCreateInput


class ParentService:
    def __init__(self):
        self.model = Parent()

    def create_parent(self, parent: ParentCreateInput):
        print(parent)
