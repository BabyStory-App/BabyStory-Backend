from fastapi import FastAPI

from apis import router as main_router
#from apis.cry import router as cry_router
from apis.parent import router as parent_router
from apis.baby import router as baby_router
from apis.raws import router as raws_router
from apis.post import router as post_router
from apis.postmain import router as postmain_router
from apis.search import router as search_router
from apis.post.comment import router as comment_router

app = FastAPI()
app.include_router(main_router)
app.include_router(parent_router)
#app.include_router(cry_router)
app.include_router(baby_router)
app.include_router(raws_router)
app.include_router(post_router)
app.include_router(postmain_router)

app.include_router(search_router)
app.include_router(comment_router)

# uvicorn main:app --host 0.0.0.0 --port 7701 --reload
