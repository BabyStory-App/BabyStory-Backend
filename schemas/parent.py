from model.types.parent import *


# class ParentCreateInput(
#     ParentType_uid,
#     ParentType_email,
#     ParentType_nickname,
# ):
#     pass

class ParentCreateInput:
    uid: str
    email: str
    nickname: str
