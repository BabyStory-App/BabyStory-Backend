from fastapi import FastAPI

from apis import router as main_router
from apis.cry import router as cry_router
from apis.parent import router as parent_router
from apis.baby import router as baby_router
from apis.raws import router as raws_router
from apis.post import router as post_router
from apis.post.pheart import router as pheart_router
from apis.post.pscript import router as pscript_router
from apis.post.pview import router as pview_router
from apis.post.pcomment import router as pcomment_router
from apis.post.pcomment.cheart import router as cheart_router
from apis.post.postmain import router as postmain_router
from apis.search import router as search_router
from apis.friend import router as friend_router
from apis.chat import router as chat_router
from apis.chat.chatroom import router as chatroom_router
from apis.diary import router as diary_router
from apis.diary.dday import router as dday_router
from apis.diary.hospital import router as hospital_router
from apis.diary.milk import router as milk_router
# from apis.aidoctor import router as aidoctor_router
from apis.alert import router as alert_router

from fastapi.staticfiles import StaticFiles
from apis.setting import router as setting_router

app = FastAPI()

app.include_router(main_router)
app.include_router(parent_router)
app.include_router(cry_router)
app.include_router(baby_router)
app.include_router(raws_router)
app.include_router(post_router)
app.include_router(pheart_router)
app.include_router(pscript_router)
app.include_router(pview_router)
app.include_router(pcomment_router)
app.include_router(cheart_router)
app.include_router(friend_router)
app.include_router(postmain_router)

app.include_router(search_router)
app.include_router(setting_router)
app.include_router(chat_router)
app.include_router(chatroom_router)
app.include_router(diary_router)
app.include_router(dday_router)
app.include_router(hospital_router)
app.include_router(milk_router)
app.mount("/qq", StaticFiles(directory="static", html=True), name="static")
# app.include_router(aidoctor_router)
app.include_router(alert_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7701)
# uvicorn main:app --host 0.0.0.0 --port 7701 --reload
