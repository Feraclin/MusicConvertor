from fastapi import APIRouter, HTTPException, Depends
from api.app.api_v1.deps import app_dependency, user_dependency, get_user_by_id
from api.app.models import UserModel
from api.app.schemas import UserNameRequest, UserRequest

router = APIRouter()


@router.post("/user/")
async def create_user(user: UserNameRequest, app=app_dependency):
    print(app.state.users)
    if not user.username:
        raise HTTPException(status_code=400)
    user: UserModel = await app.state.users.create_user(username=user.username)
    return {"access_token": user.access_token, "user_id": user.id_}


@router.get("/users/", response_model=list[str])
async def get_users(app=app_dependency) -> list[str]:
    user_list: list[UserModel] = await app.state.users.get_users_list()
    return [user.username for user in user_list]
