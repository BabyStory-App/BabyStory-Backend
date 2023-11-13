from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=[""],
    responses={404: {"description": "Not found"}},
)


# http//localhost:8000/
@router.get("/")
async def root():
    return {'hello': 'world'}
