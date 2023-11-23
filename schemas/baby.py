from model.types.baby import *
from utils.typing import PartialType


class BabySetable(
    BabyType_name,
    BabyType_gender,
    BabyType_birthDate,
    BabyType_bloodType,
):
    pass


class BabyCreateInput(
    BabyType_name,
    BabyType_gender,
    BabyType_birthDate,
    BabyType_bloodType,
):
    pass


class BabyUpdateInput(BabySetable, metaclass=PartialType):
    pass
