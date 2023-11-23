from model.types.parent import *
from utils.typing import PartialType


class ParentSetable (
    ParentType_email,
    ParentType_nickname,
    ParentType_photoId,
    ParentType_description,
):
    pass


class ParentCreateInput(
    ParentType_uid,
    ParentType_email,
    ParentType_nickname,
):
    pass


class ParentUpdateInput(ParentSetable, metaclass=PartialType):
    pass
