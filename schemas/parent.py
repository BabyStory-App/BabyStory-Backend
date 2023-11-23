from model.types.parent import *
from utils.typing import AllOptional


class ParentCreateInput(
    ParentType_uid,
    ParentType_email,
    ParentType_nickname,
):
    pass


class ParentSetable (
    ParentType_email,
    ParentType_nickname,
    ParentType_photoId,
    ParentType_description,
):
    pass


class ParentUpdateInput(ParentSetable, metaclass=AllOptional):
    pass
