from fastapi import FastAPI

from apis import router as main_router
from apis.cry import router as cry_router

app = FastAPI()
app.include_router(main_router)
app.include_router(cry_router)

# uvicorn main:app --host 0.0.0.0 --port 7701 --reload
