from model.types.baby import *
from utils.typing import PartialType


class BabySetable(
    BabyType_id,
    BabyType_name,
    BabyType_gender,
    BabyType_birthDate,
    BabyType_bloodType,
    BabyType_photoId
):
    pass


class BabyCreateInput(
    BabyType_name,
    BabyType_gender,
    BabyType_birthDate,
    BabyType_bloodType,
    BabyType_photoId
):
    pass


class BabyUpdateInput(BabySetable, metaclass=PartialType):
    pass
