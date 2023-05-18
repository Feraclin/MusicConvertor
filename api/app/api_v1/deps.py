from fastapi import Depends, Request, HTTPException

from api.app.schemas import UserRequest


async def get_app(request: Request):
    return request.app


async def check_user(u1: UserRequest, request: Request):
    user = await get_user_by_id(u1.user_id, request=request)
    if u1.access_token != user.access_token:
        raise HTTPException(status_code=403)
    return user


async def get_user_by_id(user_id: str, request: Request):
    user = await request.app.state.users.get_user_by_id(user_id)
    return user


app_dependency = Depends(get_app)
user_dependency = Depends(check_user)
