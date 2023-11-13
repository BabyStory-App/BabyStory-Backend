from fastapi import FastAPI

# from apis.todo import router as todo_router
from apis import router as main_router

app = FastAPI()
app.include_router(main_router)
# app.include_router(todo_router)
