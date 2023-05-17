
from fastapi import APIRouter
from api.app.api_v1.deps import app_dependency


router = APIRouter()


@router.post("/users/")
async def create_user(username: str, app = app_dependency):
    user = await app.state.users.create_user(username=username)
    return {"user_id": user[0], "access_token": user[1]}
